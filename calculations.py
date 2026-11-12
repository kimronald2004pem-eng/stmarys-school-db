def compute_o_level_grade(aoi_score, exam_score):
    """Computes O-Level NLSC score (20% AoI + 80% Exam)."""
    total = float(aoi_score) + float(exam_score)
    if total >= 80:
        descriptor, remark = "Outstanding", "Exceptional demonstration of core competencies."
    elif total >= 60:
        descriptor, remark = "Moderate", "Good achievement of expected learning outcomes."
    elif total >= 40:
        descriptor, remark = "Basic", "Basic attainment; requires targeted revision."
    else:
        descriptor, remark = "Below Basic", "Needs urgent academic remediation."
    return round(total, 1), descriptor, remark

def compute_tax_free_payroll(base_salary, allowances, salary_advance=0.0):
    """Calculates net payroll purely from gross earnings minus cash advances."""
    gross = float(base_salary) + float(allowances)
    net_paid = round(gross - float(salary_advance), 2)
    return {
        "gross_pay": round(gross, 2),
        "salary_advance": round(float(salary_advance), 2),
        "net_paid": net_paid
    }