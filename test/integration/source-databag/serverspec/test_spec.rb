require_relative '../../helper_spec.rb'

describe user('bbreezer') do
  it { should exist }
  it { should belong_to_group 'group2' }
  it { should belong_to_group 'group1' }
  it { should belong_to_group 'group3' }
  it { have_login_shell 'bin/bash' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCun7TGUhQ1JoWkdtroI4ufEnf/cPWn5mIitu8+eTtMK/yS71CuEhf8f6IkKMuSd5L9PHiIAYd0o87pJ952sUsDdLpk7NPhxVod7ADa7uC+FnFrJ0tgyUlPpe0XC77H1T9abpQ2fAOsC5F+fuWQSBxJyczS6tOIz7b25SUBSTA5ObM4bP0LEE2CJ4uegNpmPn73LAhYgRU43VCH4+w7QmNUHdhkcuVIVNiK2Kt7o3KXP8OjbrdQLCdG2aCMEITrTljHPazhbAgkMnEKLY28fWJpJTIzRCSdEXhdsJMS/nzszPCXvJiol6xOvbcYooYg9c9auMQJUn7EpR062VmlPXuP bbreezer1' }
  #system  : true
end

describe user('ebacardi') do
  it { should exist }
  it { should belong_to_group 'group2' }
  it { should belong_to_group 'group1' }
  it { have_login_shell 'bin/sh' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDIg6ennnJMC9Ogw55LdVZnpfiaaQLDrAQoWPeFWOld8CCql5JDARY8N+/Zr+SxxHQBb4KqXZidE73u8srEtXcS1YTlDMLK2+KIKPb8TJl4ksChBUv3XM95VDGT0AVUy4yW8v3PTKVlSA9b8yUBOcMQfDd1wtGsyL/Hjq9m0Jev+fXUV7vsVJXtV6OQOEwH8ag6NtdgQ34FdDqCUHK+vNtzrr6zXrgUj38NeAdNlb/WlaSFUlnCiRoohTk/9m3+bcne3Q84o5AzxYvB1d7azpVQFrBQABRR/hyTr07nSdBm5x4RUY35rGT4YTSrslvY+605nZon6beoK81jmcJdi9S1 ebacardi' }
end

describe user('fbacardi') do
  it { should_not exist }
end

describe user('daniels') do
  it { should_not exist }
end

describe user('whisky') do
  it { should exist }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDLql1khoXEH/pThpLSDwJNBIEHkjrBggjEvRCqCFYvE1Neavc6iuLSzjLdnj74LNrPEjY+xcjAcPmgwxo8+WKpLL7Iy8e9IGH3lwB05x9jfnw2H1ZRnZZxF+wV/ei/vfCmRyt2cqv+DLomg18RDTnyTk2pvSEvL0xkRn5QRbzxqbnB+9xmItTjdtq/ZDYRgFYn2ZPfokFyyr3KpwpK0gNcpFhCF94CvExKpu6SFPTv+ERnFvHEN9d8SlzwkyCP4yqrfOjFuVUuZf2FtAkDx0d4cXo0i7VUM/hOthUNFpmljZLhkxafPxwp50Q/xRe7MvDQMrEPGPZ/pubOwzqVmxxx' }
end
