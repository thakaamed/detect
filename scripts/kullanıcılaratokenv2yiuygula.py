cranio_package = CranioPackage.objects.first()
companys = Company.objects.all()
profiles = Profile.objects.all()
new_package_dict = {
    1: 4,
    2: 6,
    3: 5,
    4: 54,
    5: 13,
    6: 32,
    7: 53,
}
for profile in profiles:
    if not profile.company:
        new_company = Company.objects.create(
            name=profile.user.username
        )
        profile.company = new_company
        profile.save()
    cranio_buyed_obj = CranioBuyedPackage.objects.filter(company=profile.company).first()
    if cranio_buyed_obj:
        cranio_buyed_obj.profiles.add(profile)
        cranio_buyed_obj.save()
    else:
        cranio_buyed_package = CranioBuyedPackage.objects.create(
            cranio_package=cranio_package,
            company=profile.company
        )
        cranio_buyed_package.profiles.add(profile)
        cranio_buyed_package.save()


        old_buyed_package = BuyedPackage.objects.filter(company=profile.company).first()
        
        new_pack_id = new_package_dict[old_buyed_package.package.id] if old_buyed_package else 54
        token_bar = CranioTokenBar.objects.get(id=new_pack_id)
        cranio_buyed_token = CranioBuyedToken.objects.create(
            company = profile.company,
            tokenbar = token_bar
        )

        CranioRemainingToken.objects.create(
            cranio_buyed_token = cranio_buyed_token,
        )