import React from 'react';
import { SvgIcon, SvgIconProps } from '@material-ui/core';
import { ReactComponent as ChiadogeIcon } from './images/chiadoge.svg';

export default function Keys(props: SvgIconProps) {
  return <SvgIcon component={ChiadogeIcon} viewBox="0 0 200 200" {...props} />;
}
