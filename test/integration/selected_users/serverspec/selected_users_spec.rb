require_relative '../../helper_spec.rb'
require 'yaml'

describe user('daniels') do
  it { should exist }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDLql1khoXEH/pThpLSDwJNBIEHkjrBggjEvRCqCFYvE1Neavc6iuLSzjLdnj74LNrPEjY+xcjAcPmgwxo8+WKpLL7Iy8e9IGH3lwB05x9jfnw2H1ZRnZZxF+wV/ei/vfCmRyt2cqv+DLomg18RDTnyTk2pvSEvL0xkRn5QRbzxqbnB+9xmItTjdtq/ZDYRgFYn2ZPfokFyyr3KpwpK0gNcpFhCF94CvExKpu6SFPTv+ERnFvHEN9d8SlzwkyCP4yqrfOjFuVUuZf2FtAkDx0d4cXo0i7VUM/hOthUNFpmljZLhkxafPxwp50Q/xRe7MvDQMrEPGPZ/pubOwzqVmMWH' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxAqbTlltSFlRY+gQyAx3j0W+WDnahZYbECAXiwNqAHG7PP8GSEDVkfZTkJdlu9PoB/B3nW2R/Q3//IxUfzRsUnjUzl0WXbhz331n5bHtgJlg82MGqwbNjN0yMR/GB4pQKeExYOLKi/7jI/wkOAJ4X9Bv9skEK/mHAWWPrBf/5C5qWUOxVC1+he3iaU+LSbiL6uiNs8S49fiGno8tBkBFgth+9gqdCLRAFVe2dzJJK1nSQTffHCs12pJs2S3yBD9KkUQJO51tByP4qO3549iwLo8hQnqtFULMpL+NN5Muk1bFZ2jW+0Sri1bhVS58llZCuoENZsLf/+xejbfwJAk4h' }
#TODO: second key should have #key_options: no-port-forwarding
end

describe user('gin') do
  it { should exist }
  it { have_login_shell '/bin/false' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCcoo+eU8+k7QYpKbZwOQwiMpeklQcmEyLTsJr0RLTeqsHkIh8rFWyMZURDZ5pgEGo3iXZD+dqM28agy2Pw68/V0wht/9n0PjmUVZgkWIas162w3vZrJENDi8wAo4ojQJf0lZf63K8AxoB12fF+QdR7jfTLrz2bCxv9XaHKm7nYGtRO0f8ETgvwpIS2jN0mPAD7qnCFvLtbaxd/UzsQS5M8Au42+9zdn78Atm7gtKY9uR5U1Jwrop8KipXf0wAtMo39Xc9P8hGbYGA1jkbcG2x1LI7G9L+PddxeZjpkW2Uv559YJDRjBJfJAfp6K4HGV5uXITSMVDY9KBYvepolrlul' }
end

describe user('rum') do
  it { should_not exist }
end

describe user('stewart') do
  it { should_not exist }
end

describe user('vodaka') do
  it { should_not exist }
end

describe user('raki') do
  it { should_not exist }
end

## Load files from remote machine
reg_selected_users_key_vars = cat_remote_file("/tmp/reg_selected_users_key_vars.yaml")
puts " XXXX "
puts reg_selected_users_key_vars
puts  " XXXX "
reg_selected_users_vars = cat_remote_file("/tmp/reg_selected_users_vars.yaml")

describe "Database match for selected " do
  it "keys" do
    expected_hash = [{"keys"=>[{"key"=>"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCcoo+eU8+k7QYpKbZwOQwiMpeklQcmEyLTsJr0RLTeqsHkIh8rFWyMZURDZ5pgEGo3iXZD+dqM28agy2Pw68/V0wht/9n0PjmUVZgkWIas162w3vZrJENDi8wAo4ojQJf0lZf63K8AxoB12fF+QdR7jfTLrz2bCxv9XaHKm7nYGtRO0f8ETgvwpIS2jN0mPAD7qnCFvLtbaxd/UzsQS5M8Au42+9zdn78Atm7gtKY9uR5U1Jwrop8KipXf0wAtMo39Xc9P8hGbYGA1jkbcG2x1LI7G9L+PddxeZjpkW2Uv559YJDRjBJfJAfp6K4HGV5uXITSMVDY9KBYvepolrlul"}], "user"=>"gin"}, {"keys"=>[{"key"=>"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDLql1khoXEH/pThpLSDwJNBIEHkjrBggjEvRCqCFYvE1Neavc6iuLSzjLdnj74LNrPEjY+xcjAcPmgwxo8+WKpLL7Iy8e9IGH3lwB05x9jfnw2H1ZRnZZxF+wV/ei/vfCmRyt2cqv+DLomg18RDTnyTk2pvSEvL0xkRn5QRbzxqbnB+9xmItTjdtq/ZDYRgFYn2ZPfokFyyr3KpwpK0gNcpFhCF94CvExKpu6SFPTv+ERnFvHEN9d8SlzwkyCP4yqrfOjFuVUuZf2FtAkDx0d4cXo0i7VUM/hOthUNFpmljZLhkxafPxwp50Q/xRe7MvDQMrEPGPZ/pubOwzqVmMWH"}, {"key_options"=>"no-port-forwarding", "key"=>"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxAqbTlltSFlRY+gQyAx3j0W+WDnahZYbECAXiwNqAHG7PP8GSEDVkfZTkJdlu9PoB/B3nW2R/Q3//IxUfzRsUnjUzl0WXbhz331n5bHtgJlg82MGqwbNjN0yMR/GB4pQKeExYOLKi/7jI/wkOAJ4X9Bv9skEK/mHAWWPrBf/5C5qWUOxVC1+he3iaU+LSbiL6uiNs8S49fiGno8tBkBFgth+9gqdCLRAFVe2dzJJK1nSQTffHCs12pJs2S3yBD9KkUQJO51tByP4qO3549iwLo8hQnqtFULMpL+NN5Muk1bFZ2jW+0Sri1bhVS58llZCuoENZsLf/+xejbfwJAk4h"}], "user"=>"daniels"}]
    given_hash = YAML.load(reg_selected_users_key_vars)
    expect(given_hash).to match_array(expected_hash)
  end

  it "users" do
    expected_hash = [{"comment"=>"Gordons Gin", "shell"=>"/bin/false", "name"=>"gin"}, {"comment"=>"Jack daniels", "name"=>"daniels"}]
    given_hash = YAML.load(reg_selected_users_vars)
    expect(given_hash).to match_array(expected_hash)
  end

end

