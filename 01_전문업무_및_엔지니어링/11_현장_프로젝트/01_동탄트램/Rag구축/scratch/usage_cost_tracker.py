import json
import os
import time
from datetime import datetime, date
from pathlib import Path
import threading

# Gemini Official Pricing (USD per 1M tokens)
# Gemini 2.5 / 3.6 Flash:
# Input: $0.075 / 1M tokens
# Context Caching: $0.01875 / 1M tokens
# Output: $0.30 / 1M tokens
PRICE_PER_M_INPUT = 0.075
PRICE_PER_M_CACHED = 0.01875
PRICE_PER_M_OUTPUT = 0.30
USD_TO_KRW = 1380.0

# Free tier preview limits
FREE_TIER_DAILY_LIMIT = 20  # Preview/Flash models on Google AI Studio Free Tier
FREE_TIER_RPM_LIMIT = 15

class UsageCostTracker:
    def __init__(self, data_file_path=None):
        if data_file_path is None:
            data_file_path = Path(__file__).parent / "usage_stats.json"
        self.file_path = Path(data_file_path)
        self.lock = threading.Lock()
        self._ensure_file()

    def _ensure_file(self):
        if not self.file_path.exists():
            self._init_daily_stats()

    def _init_daily_stats(self):
        today_str = date.today().isoformat()
        initial_data = {
            "date": today_str,
            "daily_queries": 0,
            "daily_prompt_tokens": 0,
            "daily_candidate_tokens": 0,
            "daily_cached_tokens": 0,
            "daily_total_tokens": 0,
            "daily_cost_usd": 0.0,
            "daily_cost_krw": 0.0,
            "free_tier_status": "SAFE",
            "last_error": "",
            "history": []
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
        return initial_data

    def _load_data(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Reset daily stats if day changed
            if data.get("date") != date.today().isoformat():
                return self._init_daily_stats()
            return data
        except Exception:
            return self._init_daily_stats()

    def _save_data(self, data):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[UsageCostTracker Error] Failed to save stats: {e}")

    def record_usage(self, prompt_tokens=0, candidate_tokens=0, cached_tokens=0, model="gemini-3.6-flash", status="OK", error_code=None):
        with self.lock:
            data = self._load_data()
            
            try:
                prompt_tokens = int(prompt_tokens or 0)
            except Exception:
                prompt_tokens = 0
                
            try:
                candidate_tokens = int(candidate_tokens or 0)
            except Exception:
                candidate_tokens = 0
                
            try:
                cached_tokens = int(cached_tokens or 0)
            except Exception:
                cached_tokens = 0

            # Fallback estimation for SDK responses without token metadata
            is_estimated = False
            if prompt_tokens == 0 and candidate_tokens == 0 and status == "OK" and "local" not in str(model).lower():
                prompt_tokens = 12500
                candidate_tokens = 550
                is_estimated = True

            # Calculate cost for this query
            # Prompt tokens minus cached tokens
            active_prompt_tokens = max(0, prompt_tokens - cached_tokens)
            cost_usd = (
                (active_prompt_tokens / 1_000_000.0) * PRICE_PER_M_INPUT +
                (cached_tokens / 1_000_000.0) * PRICE_PER_M_CACHED +
                (candidate_tokens / 1_000_000.0) * PRICE_PER_M_OUTPUT
            )
            cost_krw = cost_usd * USD_TO_KRW

            # Update daily aggregates
            data["daily_queries"] += 1
            data["daily_prompt_tokens"] += prompt_tokens
            data["daily_candidate_tokens"] += candidate_tokens
            data["daily_cached_tokens"] += cached_tokens
            data["daily_total_tokens"] += (prompt_tokens + candidate_tokens)
            data["daily_cost_usd"] = round(data["daily_cost_usd"] + cost_usd, 6)
            data["daily_cost_krw"] = round(data["daily_cost_krw"] + cost_krw, 2)

            # Determine Free Tier status
            queries = data["daily_queries"]
            if error_code in [429, "429", "RESOURCE_EXHAUSTED"] or queries >= FREE_TIER_DAILY_LIMIT:
                data["free_tier_status"] = "EXCEEDED"
            elif queries >= int(FREE_TIER_DAILY_LIMIT * 0.7):
                data["free_tier_status"] = "WARNING"
            else:
                data["free_tier_status"] = "SAFE"

            if error_code:
                data["last_error"] = str(error_code)

            # Record event in history (keep last 30)
            event = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "model": model,
                "prompt_tokens": prompt_tokens,
                "candidate_tokens": candidate_tokens,
                "total_tokens": prompt_tokens + candidate_tokens,
                "cost_usd": round(cost_usd, 6),
                "cost_krw": round(cost_krw, 2),
                "status": status,
                "error_code": error_code
            }
            history = data.get("history", [])
            history.insert(0, event)
            data["history"] = history[:30]

            self._save_data(data)

            return {
                "query": {
                    "prompt_tokens": prompt_tokens,
                    "candidate_tokens": candidate_tokens,
                    "total_tokens": prompt_tokens + candidate_tokens,
                    "cost_usd": round(cost_usd, 6),
                    "cost_krw": round(cost_krw, 2),
                    "model": model,
                    "status": status
                },
                "daily": {
                    "queries": data["daily_queries"],
                    "limit": FREE_TIER_DAILY_LIMIT,
                    "remaining": max(0, FREE_TIER_DAILY_LIMIT - data["daily_queries"]),
                    "prompt_tokens": data["daily_prompt_tokens"],
                    "candidate_tokens": data["daily_candidate_tokens"],
                    "total_tokens": data["daily_total_tokens"],
                    "cost_usd": round(data["daily_cost_usd"], 4),
                    "cost_krw": round(data["daily_cost_krw"], 1),
                    "free_tier_status": data["free_tier_status"]
                }
            }

    def mark_quota_exceeded(self, model="gemini", error_detail="429 Resource Exhausted"):
        with self.lock:
            data = self._load_data()
            data["free_tier_status"] = "EXCEEDED"
            data["last_error"] = str(error_detail)
            self._save_data(data)

    def get_summary(self):
        with self.lock:
            data = self._load_data()
            queries = data["daily_queries"]
            remaining = max(0, FREE_TIER_DAILY_LIMIT - queries)
            
            # Simulated estimates for 100 queries / 1,000 queries
            avg_cost_krw = (data["daily_cost_krw"] / queries) if queries > 0 else 1.8
            est_100_krw = round(avg_cost_krw * 100, 0)
            est_1000_krw = round(avg_cost_krw * 1000, 0)

            return {
                "date": data.get("date"),
                "daily_queries": queries,
                "free_tier_limit": FREE_TIER_DAILY_LIMIT,
                "free_tier_remaining": remaining,
                "free_tier_status": data.get("free_tier_status", "SAFE"),
                "daily_total_tokens": data.get("daily_total_tokens", 0),
                "daily_prompt_tokens": data.get("daily_prompt_tokens", 0),
                "daily_candidate_tokens": data.get("daily_candidate_tokens", 0),
                "daily_cost_usd": data.get("daily_cost_usd", 0.0),
                "daily_cost_krw": data.get("daily_cost_krw", 0.0),
                "avg_query_cost_krw": round(avg_cost_krw, 2),
                "est_100_queries_krw": est_100_krw,
                "est_1000_queries_krw": est_1000_krw,
                "exchange_rate": USD_TO_KRW,
                "pricing": {
                    "input_per_m_usd": PRICE_PER_M_INPUT,
                    "input_per_m_krw": round(PRICE_PER_M_INPUT * USD_TO_KRW, 1),
                    "cached_per_m_usd": PRICE_PER_M_CACHED,
                    "cached_per_m_krw": round(PRICE_PER_M_CACHED * USD_TO_KRW, 1),
                    "output_per_m_usd": PRICE_PER_M_OUTPUT,
                    "output_per_m_krw": round(PRICE_PER_M_OUTPUT * USD_TO_KRW, 1)
                },
                "history": data.get("history", [])[:10]
            }

# Global singleton
_tracker_instance = None

def get_tracker():
    global _tracker_instance
    if _tracker_instance is None:
        _tracker_instance = UsageCostTracker()
    return _tracker_instance
