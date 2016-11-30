require_relative '../../helper_spec.rb'

describe user('daniels') do
  it { should exist }
  it { should belong_to_group 'group2' }
  it { should belong_to_group 'group1' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDLql1khoXEH/pThpLSDwJNBIEHkjrBggjEvRCqCFYvE1Neavc6iuLSzjLdnj74LNrPEjY+xcjAcPmgwxo8+WKpLL7Iy8e9IGH3lwB05x9jfnw2H1ZRnZZxF+wV/ei/vfCmRyt2cqv+DLomg18RDTnyTk2pvSEvL0xkRn5QRbzxqbnB+9xmItTjdtq/ZDYRgFYn2ZPfokFyyr3KpwpK0gNcpFhCF94CvExKpu6SFPTv+ERnFvHEN9d8SlzwkyCP4yqrfOjFuVUuZf2FtAkDx0d4cXo0i7VUM/hOthUNFpmljZLhkxafPxwp50Q/xRe7MvDQMrEPGPZ/pubOwzqVmMWH' }

  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxAqbTlltSFlRY+gQyAx3j0W+WDnahZYbECAXiwNqAHG7PP8GSEDVkfZTkJdlu9PoB/B3nW2R/Q3//IxUfzRsUnjUzl0WXbhz331n5bHtgJlg82MGqwbNjN0yMR/GB4pQKeExYOLKi/7jI/wkOAJ4X9Bv9skEK/mHAWWPrBf/5C5qWUOxVC1+he3iaU+LSbiL6uiNs8S49fiGno8tBkBFgth+9gqdCLRAFVe2dzJJK1nSQTffHCs12pJs2S3yBD9KkUQJO51tByP4qO3549iwLo8hQnqtFULMpL+NN5Muk1bFZ2jW+0Sri1bhVS58llZCuoENZsLf/+xejbfwJAk4h' }
  #key_options : 'no-port-forwarding'
end

describe user('vodka') do
  it { should exist }
  it { should have_uid 3300 }
  it { should belong_to_group 'group2' }
  it { should belong_to_group 'group1' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2Pq3M7AgeBjmNII6HGsKd2uaXFIfaljpNg1Rf6y3iGP84wC82bMfZTSIhnzJ4qwHj7Bzn8oiMmqtyeGcmEwLXm5f7mk3lj9NmxUEfbuWsPoSX4VHIney0F2cjrYRAHua8vZ50OrqYvRaBNttx+pCsub/Kw/t91PQvz7s5ML12DfhlfbE5f/g+ZrKHBxsn6Vw0VqN1Cx5cecaN+9NbdwTV25/RVsXC6v9TQlIqWR+znt4ZVxUSCTAbGc51tmauoleZee2XBkAO7xmJ7zPQEndhErq/zm0euZGx1xGIjQ7dVBK8t1ah2UdBS4pSHgjhDulo0hr4gIubQ0FSV+8cWCNN' }
end

describe user('pepsi') do
  it { should exist }
  it { should have_uid 3400 }
  it { have_login_shell '/bin/false' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCcoo+eU8+k7QYpKbZwOQwiMpeklQcmEyLTsJr0RLTeqsHkIh8rFWyMZURDZ5pgEGo3iXZD+dqM28agy2Pw68/V0wht/9n0PjmUVZgkWIas162w3vZrJENDi8wAo4ojQJf0lZf63K8AxoB12fF+QdR7jfTLrz2bCxv9XaHKm7nYGtRO0f8ETgvwpIS2jN0mPAD7qnCFvLtbaxd/UzsQS5M8Au42+9zdn78Atm7gtKY9uR5U1Jwrop8KipXf0wAtMo39Xc9P8hGbYGA1jkbcG2x1LI7G9L+PddxeZjpkW2Uv559YJDRjBJfJAfp6K4HGV5uXITSMVDY9KBYvepolrlul' }
end

describe user('coca') do
  it { should exist }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC2EAA1ycAADAAAQABABAQCootXD63hexEQnbCmKGC7DjFSWxkqJ2neaC5S6POEdgwo7jQ60JWy0VCm5JS5d2ZNDQh+vi1wZ2cTr6n9X9bAkYhQ/eACmzYBjf8I8AXcqaigAOjRMLADU2qQfZmnRGyOLaGDI/EH52yBjeZHbgQdJOGrB07qgAu2facA2bd6kvI8eLwCx5yjqA+mInYEewRYrr5tUduGFdPhmyoKSGpaEeWWkLhafTj9eGRMSB3unBcMtux+LxXH4TfWgVBmWNVbr2Mcv+M6tYxix/iKniBLBUH/AfM/dTHlk38y2mjemUMUc/HBW+HmH3NXMwOks8po6Iohh8JNhywUlLKN9MvB7' }
end

describe user('stewart') do
  it { should_not exist }
end

describe user('raki') do
  it { should_not exist }
end

describe user('label') do
  it { should_not exist }
end