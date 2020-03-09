# -*- coding: utf-8 -*-



def regmail(user, password):


    regmail_temp = "<h1 style='text-align:center'>Eazy Crypto Investments</h1><br><p><strong>Congratulations on setting up your brand new Eazy Crypto Investment Account.</strong></p><p>Here are your login credentials:</p><p>User name: <strong>%s</strong></p>" %user + "<p>Password: <strong>%s</strong></p>" %password + "<h6 style='text-align:center'> <strong>CFDs are complex instruments and come with a high risk of losing money rapidly due to leverage. 4% of retail investor accounts lose money when trading CFDs with this provider. You should consider whether you understand how CFDs work and whether you can afford to take the high risk of losing your money. EazyCrypto limited is authorised and regulated by the UK Financial Conduct Authority (FRN 524217) with its registered and trading office at Level 37, One Canada Square, Canary Wharf, E14 5AA, London, United Kingdom (company number 07265448).Copyright 2020 © EazyCrypto</strong></h6>"


    return regmail_temp

def depmail(user):


    depositmail_temp = "<h1 style='text-align:center'>Eazy Crypto Investments</h1><br><p><strong>Your Deposit has been succsesfully initiated</strong></p><p>Please allow up to 24 hours for the funds to reflect on your trading account, our financial department is working on recieving the funds you have sent to the designated wallet and will update your account shortly</p><p>User name: <strong>%s</strong></p>" %user + "<p>Deposit Wallet: <strong>14L2PvRsAys8tKS8nihT5kderEvDi5M2PK</strong></p><h6 style='text-align:center;padding-top:10px;'> <strong>CFDs are complex instruments and come with a high risk of losing money rapidly due to leverage. 4% of retail investor accounts lose money when trading CFDs with this provider. You should consider whether you understand how CFDs work and whether you can afford to take the high risk of losing your money. EazyCrypto limited is authorised and regulated by the UK Financial Conduct Authority (FRN 524217) with its registered and trading office at Level 37, One Canada Square, Canary Wharf, E14 5AA, London, United Kingdom (company number 07265448).Copyright 2020 © EazyCrypto</strong></h6>"

    return depositmail_temp

def wdmail(user, withdraw):

    wdmail_temp ="<h1 style='text-align:center'>Eazy Crypto Investments</h1><br><p><strong>Your Withdraw has been succsesfully initiated</strong></p><p>Please allow up to 24 hours for the funds to reflect on the wallet you used for recieving the funds, our financial department is working on releasing the funds from your trading account and will update your account shortly</p><p>User name: <strong>%s</strong></p>" %user + "<p>Withdrawal Amount: <strong>%s</strong>$ USD</p>" %withdraw + "<h6 style='text-align:center;padding-top:10px;'> <strong>CFDs are complex instruments and come with a high risk of losing money rapidly due to leverage. 4% of retail investor accounts lose money when trading CFDs with this provider. You should consider whether you understand how CFDs work and whether you can afford to take the high risk of losing your money. EazyCrypto limited is authorised and regulated by the UK Financial Conduct Authority (FRN 524217) with its registered and trading office at Level 37, One Canada Square, Canary Wharf, E14 5AA, London, United Kingdom (company number 07265448).Copyright 2020 © EazyCrypto</strong></h6>"

    return wdmail_temp

def contactmail(user):

    contactmail_temp = "<p>hey, %s</p><br>" %user + "<p>Thank you for contacting Eazy Crypto, our team are working on your request, please allow up to 24 hours to respond.</p><h6 style='text-align:center'> <strong>CFDs are complex instruments and come with a high risk of losing money rapidly due to leverage. 4% of retail investor accounts lose money when trading CFDs with this provider. You should consider whether you understand how CFDs work and whether you can afford to take the high risk of losing your money. EazyCrypto limited is authorised and regulated by the UK Financial Conduct Authority (FRN 524217) with its registered and trading office at Level 37, One Canada Square, Canary Wharf, E14 5AA, London, United Kingdom (company number 07265448).Copyright 2020 © EazyCrypto</strong></h6>"

    return contactmail_temp
