# Welcome to Fake_VN_User!
### Created by NeV3RmI

A python library help you to generate Fake VN User which include: name, dob, username, password, email, phone number, user agent.

Website: [https:// picks.work](https://picks.work)
Email: admin@picks.work

# Install

    pip install fake_vn_user

## Dependent library

Random

	pip install random

Fake_useragent

	pip install fake_useragent 

# How to use

    import fake_vn_user
    
    vnuser =  fake_vn_user.get_profile()

Example Return

     {
       "sex":"nu",
       "first_name":"Vân Trang",
       "first_name_ra":"Van Trang",
       "last_name":"Phan",
       "last_name_ra":"Phan",
       "full_name":"Phan Vân Trang",
       "full_name_ra":"Phan Van Trang",
       "country_calling_code":"+84",
       "phone_provider":"mobiphone",
       "phone_number":"0907860597",
       "phone_activate":"+84564169581",
       "dob":"12-10-1912",
       "day":12,
       "month":10,
       "year":1912,
       "age":109,
       "username":"phanvantrang12101912",
       "password":"*sySYi7fAi}3b+",
       "email_provider":"vi.emailfake.com",
       "email_domain":"@epubea.site",
       "email":"phanvantrang12101912@epubea.site",
       "user_agent":"Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0",
       "ads":"Please check https://picks.work for more information, this product is created by NeV3RmI.",
       "version":"1.0.0"
    }
