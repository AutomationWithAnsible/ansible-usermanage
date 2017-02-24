require_relative '../../helper_spec.rb'

describe user('daniels') do
  it { should exist }
end

describe user('gin') do
  it { should exist }
end
