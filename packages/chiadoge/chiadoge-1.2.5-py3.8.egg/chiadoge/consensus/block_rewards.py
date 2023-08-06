from chiadoge.util.ints import uint32, uint64

# 1 Chiadoe coin = 1,000,000,000= 10 billion mojo.
_mojo_per_chiadoge = 1000000000
_blocks_per_year = 1681920  # 32 * 6 * 24 * 365


def calculate_pool_reward(height: uint32) -> uint64:
    """
    Returns the pool reward at a certain block height. The pool earns 7/8 of the reward in each block. If the farmer
    is solo farming, they act as the pool, and therefore earn the entire block reward.
    These halving events will not be hit at the exact times
    (3 years, etc), due to fluctuations in difficulty. They will likely come early, if the network space and VDF
    rates increase continuously.
    """

    if height == 0:
        return uint64(int((7 / 8) * 21000000000 * _mojo_per_chiadoge))
    elif height < 3 * _blocks_per_year:
        return uint64(int((7 / 8) * 2 * 10000 * _mojo_per_chiadoge))
    elif height < 6 * _blocks_per_year:
        return uint64(int((7 / 8) * 1 * 10000 * _mojo_per_chiadoge))
    elif height < 9 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.5 * 10000 * _mojo_per_chiadoge))
    elif height < 12 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.25 * 10000 * _mojo_per_chiadoge))
    elif height < 15 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.125 * 10000 * _mojo_per_chiadoge))
    elif height < 18 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.0625 * 10000 * _mojo_per_chiadoge))
    elif height < 21 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.03125 * 10000 * _mojo_per_chiadoge))
    elif height < 24 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.015625 * 10000 * _mojo_per_chiadoge))
    elif height < 27 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.0078125 * 10000 * _mojo_per_chiadoge))
    elif height < 30 * _blocks_per_year:
        return uint64(int((7 / 8) * 0.00390625 * 10000 * _mojo_per_chiadoge))
    elif height < 99 * _blocks_per_year:
        return uint64(int((7 / 8) * 50 * _mojo_per_chiadoge))
    else:
        return uint64(0)

def calculate_base_farmer_reward(height: uint32) -> uint64:
    """
    Returns the base farmer reward at a certain block height.
    The base fee reward is 1/8 of total block reward

    Returns the coinbase reward at a certain block height. These halving events will not be hit at the exact times
    (3 years, etc), due to fluctuations in difficulty. They will likely come early, if the network space and VDF
    rates increase continuously.
    """
    if height == 0:
        return uint64(int((1 / 8) * 21000000000 * _mojo_per_chiadoge))
    elif height < 3 * _blocks_per_year:
        return uint64(int((1 / 8) * 2 * 10000 * _mojo_per_chiadoge))
    elif height < 6 * _blocks_per_year:
        return uint64(int((1 / 8) * 1 * 10000 * _mojo_per_chiadoge))
    elif height < 9 * _blocks_per_year:
        return uint64(int((1 / 8) * 0.5 * 10000 * _mojo_per_chiadoge))
    elif height < 12 * _blocks_per_year:
        return uint64(int((1 / 8) * 0.25 * 10000 * _mojo_per_chiadoge))
    elif height < 15 * _blocks_per_year:
        return uint64(int((1 / 8) * 0.125 * 10000 * _mojo_per_chiadoge))
    elif height < 18 * _blocks_per_year:
        return uint64(int((1 / 8) * 0.0625 * 10000 * _mojo_per_chiadoge))
    elif height < 21 * _blocks_per_year:
        return uint64(int((1 / 8) * 0.03125 * 10000 * _mojo_per_chiadoge))
    elif height < 24 * _blocks_per_year:
        return uint64(int((1 / 8) * 0.015625 * 10000 * _mojo_per_chiadoge))
    elif height < 27 * _blocks_per_year:
        return uint64(int((1 / 8) * 0.0078125 * 10000 * _mojo_per_chiadoge))
    elif height < 30 * _blocks_per_year:
        return uint64(int((1 / 8) * 0.00390625 * 10000 * _mojo_per_chiadoge))
    elif height < 99 * _blocks_per_year:
        return uint64(int((1 / 8) * 50 * _mojo_per_chiadoge))
    else:
        return uint64(0)
