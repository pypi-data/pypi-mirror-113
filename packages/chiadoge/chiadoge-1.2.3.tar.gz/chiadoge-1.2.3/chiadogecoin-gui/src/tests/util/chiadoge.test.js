const chiadoge = require('../../util/chiadoge');

describe('chiadoge', () => {
  it('converts number mojo to chiadoge', () => {
    const result = chiadoge.mojo_to_chiadoge(1000000);

    expect(result).toBe(0.000001);
  });
  it('converts string mojo to chiadoge', () => {
    const result = chiadoge.mojo_to_chiadoge('1000000');

    expect(result).toBe(0.000001);
  });
  it('converts number mojo to chiadoge string', () => {
    const result = chiadoge.mojo_to_chiadoge_string(1000000);

    expect(result).toBe('0.000001');
  });
  it('converts string mojo to chiadoge string', () => {
    const result = chiadoge.mojo_to_chiadoge_string('1000000');

    expect(result).toBe('0.000001');
  });
  it('converts number chiadoge to mojo', () => {
    const result = chiadoge.chiadoge_to_mojo(0.000001);

    expect(result).toBe(1000000);
  });
  it('converts string chiadoge to mojo', () => {
    const result = chiadoge.chiadoge_to_mojo('0.000001');

    expect(result).toBe(1000000);
  });
  it('converts number mojo to colouredcoin', () => {
    const result = chiadoge.mojo_to_colouredcoin(1000000);

    expect(result).toBe(1000);
  });
  it('converts string mojo to colouredcoin', () => {
    const result = chiadoge.mojo_to_colouredcoin('1000000');

    expect(result).toBe(1000);
  });
  it('converts number mojo to colouredcoin string', () => {
    const result = chiadoge.mojo_to_colouredcoin_string(1000000);

    expect(result).toBe('1,000');
  });
  it('converts string mojo to colouredcoin string', () => {
    const result = chiadoge.mojo_to_colouredcoin_string('1000000');

    expect(result).toBe('1,000');
  });
  it('converts number colouredcoin to mojo', () => {
    const result = chiadoge.colouredcoin_to_mojo(1000);

    expect(result).toBe(1000000);
  });
  it('converts string colouredcoin to mojo', () => {
    const result = chiadoge.colouredcoin_to_mojo('1000');

    expect(result).toBe(1000000);
  });
});
