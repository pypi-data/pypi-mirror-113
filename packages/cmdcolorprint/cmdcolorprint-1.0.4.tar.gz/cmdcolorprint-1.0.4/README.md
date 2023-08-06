<h1>
cmdcolorprint
</h1>

使い方 How to use

cmdでは

cmdcolorprint test greenで緑色でtestが出力でき、

python内では

import cmdcolorprint

cmdcolorprint.color_print.Color.output_color.cprint_name("test","green")

または

import cmdcolorprint

cmdcolorprint.color_print.Color.output_color.color_print("test",0x0002)

で緑色でtestを出力出来ます。

説明以上!