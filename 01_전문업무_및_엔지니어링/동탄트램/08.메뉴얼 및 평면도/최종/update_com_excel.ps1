$excel = [System.Runtime.InteropServices.Marshal]::GetActiveObject('Excel.Application')
$wb = $null
foreach ($b in $excel.Workbooks) {
    if ($b.Name -like "*매뉴얼 BODY*") {
        $wb = $b
        break
    }
}

if ($wb) {
    $ws = $wb.Worksheets.Item('통신분야')
    
    $ws.Cells.Item(8, 10).Value2 = "1) 투입 자원 사전 검토: 통신 공사 투입 인력, 광융착기/OTDR 측정장비, 자재 수급 계획 등 타당성/적합성 검토함`n2) 적합성 확보: 시스템업체/협력업체 및 감리단 주관으로 공정별 인력 및 장비 투입 제출서의 적합성을 최종 승인함"
    $ws.Hyperlinks.Add($ws.Cells.Item(8, 11), "매뉴얼BODY(집행단계-첨부폴더)\통신분야\8_자재 인력 장비 등 투입 사전 검토\표준서\자재 인력 장비 등 투입 사전 검토_표준서.html", $null, $null, "📄 [더블클릭] 표준서 열기 🔗")
    
    $ws.Cells.Item(8, 12).Value2 = "1) 자원 투입 수급: 공정별 숙련 통신공 투입, 광융착기/OTDR 시험 장비 검교정 상태 확인`n2) 안전/민원 대책: 현장 자재 야적장 확보, 도로 굴착시 교통통제 및 민원 대장 대책을 종합 검토함"
    $ws.Hyperlinks.Add($ws.Cells.Item(8, 13), "매뉴얼BODY(집행단계-첨부폴더)\통신분야\8_자재 인력 장비 등 투입 사전 검토\수행지침\자재 인력 장비 등 투입 사전 검토_수행지침.html", $null, $null, "📄 [더블클릭] 수행지침 열기 🔗")

    $ws.Cells.Item(8, 14).Value2 = "1) 공정별 숙련 인력 투입 계획 및 정밀 측정 장비(OTDR, 융착기) 검교정 상태를 확인하였는가?`n2) 자재 수급 계획, 야적장 확보 및 민원 대책을 포함한 투입 계획서를 작성하였는가?"
    $ws.Hyperlinks.Add($ws.Cells.Item(8, 15), "매뉴얼BODY(집행단계-첨부폴더)\통신분야\8_자재 인력 장비 등 투입 사전 검토\체크리스트\자재 인력 장비 등 투입 사전 검토_체크리스트.html", $null, $null, "📄 [더블클릭] 체크리스트 열기 🔗")

    $wb.Save()
    Write-Host "🎉 EXCEL COM OBJECT UPDATED & SAVED SUCCESSFULLY!"
} else {
    Write-Host "Excel application not currently active with target workbook."
}
