require_relative '../../helper_spec.rb'

describe user('bbreezer') do
  it { should_not exist }
end


describe user('sartois') do
  it { should exist }
  it { should belong_to_group 'group2' }
  it { should belong_to_group 'group1' }
  it { should belong_to_group 'group3' }
  it { have_login_shell 'bin/bash' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCun7TGUhQ1JoWkdtroI4ufEnf/cPWn5mIitu8+eTtMK/yS71CuEhf8f6IkKMuSd5L9PHiIAYd0o87pJ952sUsDdLpk7NPhxVod7ADa7uC+FnFrJ0tgyUlPpe0XC77H1T9abpQ2fAOsC5F+fuWQSBxJyczS6tOIz7b25SUBSTA5ObM4bP0LEE2CJ4uegNpmPn73LAhYgRU43VCH4+w7QmNUHdhkcuVIVNiK2Kt7o3KXP8OjbrdQLCdG2aCMEITrTljHPazhbAgkMnEKLY28fWJpJTIzRCSdEXhdsJMS/nzszPCXvJiol6xOvbcYooYg9c9auMQJUn7EpR062VmlPXuP bbreezer1' }
  #system  : true
end