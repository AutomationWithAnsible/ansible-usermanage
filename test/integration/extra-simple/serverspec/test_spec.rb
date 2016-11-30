require_relative '../../helper_spec.rb'
require 'yaml'

describe user('daniels2') do
  it { should exist }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDLql1khoXEH/pThpLSDwJNBIEHkjrBggjEvRCqCFYvE1Neavc6iuLSzjLdnj74LNrPEjY+xcjAcPmgwxo8+WKpLL7Iy8e9IGH3lwB05x9jfnw2H1ZRnZZxF+wV/ei/vfCmRyt2cqv+DLomg18RDTnyTk2pvSEvL0xkRn5QRbzxqbnB+9xmItTjdtq/ZDYRgFYn2ZPfokFyyr3KpwpK0gNcpFhCF94CvExKpu6SFPTv+ERnFvHEN9d8SlzwkyCP4yqrfOjFuVUuZf2FtAkDx0d4cXo0i7VUM/hOthUNFpmljZLhkxafPxwp50Q/xRe7MvDQMrEPGPZ/pubOwzqVmMWH' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxAqbTlltSFlRY+gQyAx3j0W+WDnahZYbECAXiwNqAHG7PP8GSEDVkfZTkJdlu9PoB/B3nW2R/Q3//IxUfzRsUnjUzl0WXbhz331n5bHtgJlg82MGqwbNjN0yMR/GB4pQKeExYOLKi/7jI/wkOAJ4X9Bv9skEK/mHAWWPrBf/5C5qWUOxVC1+he3iaU+LSbiL6uiNs8S49fiGno8tBkBFgth+9gqdCLRAFVe2dzJJK1nSQTffHCs12pJs2S3yBD9KkUQJO51tByP4qO3549iwLo8hQnqtFULMpL+NN5Muk1bFZ2jW+0Sri1bhVS58llZCuoENZsLf/+xejbfwJAk4h' }
#TODO: second key should have #key_options: no-port-forwarding
end

describe user('gin2') do
  it { should exist }
  it { have_login_shell '/bin/false' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCcoo+eU8+k7QYpKbZwOQwiMpeklQcmEyLTsJr0RLTeqsHkIh8rFWyMZURDZ5pgEGo3iXZD+dqM28agy2Pw68/V0wht/9n0PjmUVZgkWIas162w3vZrJENDi8wAo4ojQJf0lZf63K8AxoB12fF+QdR7jfTLrz2bCxv9XaHKm7nYGtRO0f8ETgvwpIS2jN0mPAD7qnCFvLtbaxd/UzsQS5M8Au42+9zdn78Atm7gtKY9uR5U1Jwrop8KipXf0wAtMo39Xc9P8hGbYGA1jkbcG2x1LI7G9L+PddxeZjpkW2Uv559YJDRjBJfJAfp6K4HGV5uXITSMVDY9KBYvepolrlul' }
end

describe user('rum2') do
  it { should exist }
  it { should_not have_authorized_key 'ssh-rsa AAAAB3NzaC2EAA1ycAADAAAQABABAQCootXD63hexEQnbCmKGC7DjFSWxkqJ2neaC5S6POEdgwo7jQ60JWy0VCm5JS5d2ZNDQh+vi1wZ2cTr6n9X9bAkYhQ/eACmzYBjf8I8AXcqaigAOjRMLADU2qQfZmnRGyOLaGDI/EH52yBjeZHbgQdJOGrB07qgAu2facA2bd6kvI8eLwCx5yjqA+mInYEewRYrr5tUduGFdPhmyoKSGpaEeWWkLhafTj9eGRMSB3unBcMtux+LxXH4TfWgVBmWNVbr2Mcv+M6tYxix/iKniBLBUH/AfM/dTHlk38y2mjemUMUc/HBW+HmH3NXMwOks8po6Iohh8JNhywUlLKN9MvB7' }
end

describe user('stewart2') do
  it { should exist }
  it { should have_home_directory '/opt/stewart' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDhiDPE4S4K6AGJFRSIB5xVoIlKtgjVUVHK1WhT0hD/I3nZ3AFszqDXUz4eREDlPSfMsvNCuAd1Mxwg2vx1Udbzf0M5OH1DDgYyVeJXXB5/B2rpX7vm0A1Hxx17mMHg9OrCNKNn8B83g6IqAGM6P3VKHqnRQ9kLpPcki65gMx06R2dQ1Dh5kks2yOjyx7Mjut0rL9Ig/b9ysMMC1YjMupC8vb31Dhy8pVi1F/RT/7M6PwM4Kjh3fdzgqvQRxDrmky8kbXJj+TXU6pIM1mZtZyENddUCA0rDNtpi6yIaAR9aJkcPXxPpblkWjYAO++sukz88BKWt0Z+nLx9JUhwXtoW7' }
end

describe user('vodaka2') do
  it { should exist }
  it { should have_uid 5300 }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2Pq3M7AgeBjmNII6HGsKd2uaXFIfaljpNg1Rf6y3iGP84wC82bMfZTSIhnzJ4qwHj7Bzn8oiMmqtyeGcmEwLXm5f7mk3lj9NmxUEfbuWsPoSX4VHIney0F2cjrYRAHua8vZ50OrqYvRaBNttx+pCsub/Kw/t91PQvz7s5ML12DfhlfbE5f/g+ZrKHBxsn6Vw0VqN1Cx5cecaN+9NbdwTV25/RVsXC6v9TQlIqWR+znt4ZVxUSCTAbGc51tmauoleZee2XBkAO7xmJ7zPQEndhErq/zm0euZGx1xGIjQ7dVBK8t1ah2UdBS4pSHgjhDulo0hr4gIubQ0FSV+8cWCNN' }
end

describe user('raki2') do
  it { should_not exist }
end

## Load files from remote machine
extra_simple_extra_db = cat_remote_file("/tmp/extra_simple_extra_db.yaml")
extra_simple_users_db = cat_remote_file("/tmp/extra_simple_users_db.yaml")

describe "Database match" do
  it "extra variables" do
    expected_hash = [{"state"=>"present", "vpn"=>true, "name"=>"vodaka2"}, {"state"=>"absent", "aws"=>true, "aws_group"=>"Admin", "name"=>"raki2"}]
    given_hash = YAML.load(extra_simple_extra_db)
    expect(given_hash).to match(expected_hash)
  end

  it "users variables" do
    expected_hash = [{"comment"=>"Brad", "name"=>"brad2"}, {"comment"=>"Daniel Stewart", "home"=>"/opt/stewart", "name"=>"stewart2"}, {"comment"=>"Jack daniels", "name"=>"daniels2"}, {"comment"=>"Gordons Gin", "name"=>"gin2", "shell"=>"/bin/false"}, {"comment"=>"Pirates Grog Rum", "name"=>"rum2"}, {"comment"=>"Savvy Vodka", "name"=>"vodaka2", "uid"=>5300}, {"comment"=>"Yeni Raki", "name"=>"raki2", "state"=>"absent", "uid"=>5400}]
    given_hash = YAML.load(extra_simple_users_db)
    print given_hash
    expect(given_hash).to match(expected_hash)
  end

end