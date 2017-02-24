require_relative '../../helper_spec.rb'

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
