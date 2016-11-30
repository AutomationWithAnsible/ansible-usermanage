require_relative '../../helper_spec.rb'

describe user('user1_yaml') do
  it { should exist }
  it { have_login_shell '/bin/true' }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDfIG0Zqxtj+OGordHLn82CWzRXA3++D5BdevRx7kCJE50gRhuUbc2lImBbLE+1JRlzwpg+a1AWbM1MTiHJyLbw7e4+KxfUaPxclktvrCD3xqN/Pn0ncgCcZNFrXfeP4RbHN143qzy8ri0Vn4o/3OYK9KZGkfIT+ix8TpD6804LLjrgmgFcEDxJILFNeVL187vfoGdhh/Wed4JMZSWjiXMjA9WHzFkYDWW6HhlmmjNrXQvaQTWpmDAABvP918N7LLf8KuhTcXfyWrVOCpc0jNZKOtzvScixOi2licUkJ/xlGYbirr8cmV9gS+5UzUdzMstZeiKNXkU7imcInsSk5BFv yaml1' }
end

describe user('user2_yaml') do
  it { should exist }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDXfwZI7qSBnqEwlxWFBQt9YpdhR7bHYbtcRuy77EmAu1VPZmfn+pIDLUXn5sTOZQxzXN32GohJOlC8vW63WMnROVRlI3yVjspcmxEcHeATsFEKfg2JDdH2m88fiG2JaVFBnV9N/obfGZiWCRxmjodttyETw/nvTzAQTczvalO0lm0bkfgkiGffFREucQikf+ZRbgRQmIZxNX2dYMN5nNIcRXjv+2z//N30J22Lzmo0JXRmByBIkCG+QVrvc3UudJ2prkebDp60CoTiPgA9nnpLxYbBbX4QU/q/sYTwb/wMv8g+4AENEJ8RWPIcpLXt65vTUcpbPTuEM8egfSDtlwph yaml2' }
end

describe user('user3_json') do
  it { should exist }
  it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDY3q7JKLPiPawSUK6NIJWKMl1EV9ORJkqrMIQsxanYQyElWw3Y+aj9Kbtl37hbQIYtHVb2y43e26MjlY8XfpHGRtKxtR6t+oIgxVNV3paT31OkJSiLgNS8yn7+JbyeTSu7UN2XdPZgSIF8yCWmNFvwRkW+TsRwCobXJqDwzhSx/BphLqR9ADV+nCyfhG3T/BgJ8XWsio60cOTl/Qy9aIcyDOdsu/HJtB7hIAfxbSMksocMnssJYds3wMQnNYwGVEbHVzJk8priR8GsGBgT8Bh83JmB+gDBXEfT4hRfJ0eC4ekwLAH/bg9IZhfOOQJMQHdk16HL32XNM3TPQiy9845D user3_json' }
end

