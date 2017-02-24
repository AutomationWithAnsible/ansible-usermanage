require_relative '../../helper_spec.rb'

ansible_version=`ansible --version`

puts "ANSIBLE_VERSION=", ansible_version
puts "AND THE THING IS=", ansible_version[/ansible 2.[01]./,].nil?

unless ansible_version[/ansible 2.[01]./,].nil?

  describe group('group1') do
    it { should exist }
  end

  describe group('group2') do
    it { should exist }
  end

  describe group('group3') do
    it { should exist }
  end

  describe user('daniels') do
    it { should exist }
  end

  describe user('gin') do
    it { should exist }
  end

end
