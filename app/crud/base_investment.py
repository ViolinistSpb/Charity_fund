from datetime import datetime


def base_investmemt(project, donation, session):
    donation_have = donation.full_amount - donation.invested_amount
    project_needs = project.full_amount - project.invested_amount
    if donation_have <= project_needs:
        project.invested_amount += donation_have
        donation.invested_amount += donation_have
        donation.fully_invested = True
        donation.close_date = datetime.utcnow()
        if donation_have == project_needs:
            project.fully_invested = True
            project.close_date = datetime.utcnow()
        session.add(donation, project)

    elif donation_have > project_needs:
        project.invested_amount += project_needs
        project.fully_invested = True
        project.close_date = datetime.utcnow()
        donation.invested_amount += project_needs
        session.add(donation, project)