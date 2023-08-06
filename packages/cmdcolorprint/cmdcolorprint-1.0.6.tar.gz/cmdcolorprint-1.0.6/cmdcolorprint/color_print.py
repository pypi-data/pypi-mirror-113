from ctypes import windll, Structure, byref, wintypes

class cutil:
    stdout_handle = windll.kernel32.GetStdHandle(-11)
    GetConsoleInfo = windll.kernel32.GetConsoleScreenBufferInfo
    SetConsoleAttribute = windll.kernel32.SetConsoleTextAttribute
 
    class console_screen_buffer_info(Structure):
        _fields_ = [("dwSize", wintypes._COORD),
                    ("dwCursorPosition", wintypes._COORD),
                    ("wAttributes", wintypes.WORD),
                    ("srWindow", wintypes.SMALL_RECT),
                    ("dwMaximumWindowSize", wintypes._COORD)]

class Color():

    class Color_list():
        def Color():
            """The color list"""
            colors={
            "black":"0000",
            "blue":"0001",
            "green":"0002",
            "skyblue":"0003",
            "red":"0004",
            "purple":"0005",
            "yellow":"0006",
            "white":"0007",
            "gray":"0008",
            "blue2":"0009",

            "black_label_black":"0000",
            "black_label_blue":"0001",
            "black_label_green":"0002",
            "black_label_skyblue":"0003",
            "black_label_red":"0004",
            "black_label_purple":"0005",
            "black_label_yellow":"0006",
            "black_label_white":"0007",
            "black_label_gray":"0008",
            "black_label_blue2":"0009",

            "blue_label_black":"0010",
            "blue_label_blue":"0011",
            "blue_label_green":"0012",
            "blue_label_skyblue":"0013",
            "blue_label_red":"0014",
            "blue_label_purple":"0015",
            "blue_label_yellow":"0016",
            "blue_label_white":"0017",
            "blue_label_gray":"0018",
            "blue_label_blue2":"0019",

            "green_label_black":"0020",
            "green_label_blue":"0021",
            "green_label_green":"0022",
            "green_label_skyblue":"0023",
            "green_label_red":"0024",
            "green_label_purple":"0025",
            "green_label_yellow":"0026",
            "green_label_white":"0027",
            "green_label_gray":"0028",
            "green_label_blue2":"0029",

            "skyblue_label_black":"0030",
            "skyblue_label_blue":"0031",
            "skyblue_label_green":"0032",
            "skyblue_label_skyblue":"0033",
            "skyblue_label_red":"0034",
            "skyblue_label_purple":"0035",
            "skyblue_label_yellow":"0036",
            "skyblue_label_white":"0037",
            "skyblue_label_gray":"0038",
            "skyblue_label_blue2":"0039",

            "red_label_black":"0040",
            "red_label_blue":"0041",
            "red_label_green":"0042",
            "red_label_skyblue":"0043",
            "red_label_red":"0044",
            "red_label_purple":"0045",
            "red_label_yellow":"0046",
            "red_label_white":"0047",
            "red_label_gray":"0048",
            "red_label_blue2":"0049",

            "purple_label_black":"0050",
            "purple_label_blue":"0051",
            "purple_label_green":"00522",
            "purple_label_skyblue":"0053",
            "purple_label_red":"0054",
            "purple_label_purple":"0055",
            "purple_label_yellow":"0056",
            "purple_label_white":"00557",
            "purple_label_gray":"0058",
            "purple_label_blue2":"0059",

            "yellow_label_black":"0060",
            "yellow_label_blue":"0061",
            "yellow_label_green":"0062",
            "yellow_label_skyblue":"0063",
            "yellow_label_red":"0064",
            "yellow_label_purple":"0065",
            "yellow_label_yellow":"0066",
            "yellow_label_white":"0067",
            "yellow_label_gray":"0068",
            "yellow_label_blue2":"0069",

            "white_label_black":"0070",
            "white_label_blue":"0071",
            "white_label_green":"0072",
            "white_label_skyblue":"0073",
            "white_label_red":"0074",
            "white_label_purple":"0075",
            "white_label_yellow":"0076",
            "white_label_white":"0077",
            "white_label_gray":"0078",
            "white_label_blue2":"0079",

            "gray_label_black":"0080",
            "gray_label_blue":"0081",
            "gray_label_green":"0082",
            "gray_label_skyblue":"0083",
            "gray_label_red":"0084",
            "gray_label_purple":"0085",
            "gray_label_yellow":"0086",
            "gray_label_white":"0087",
            "gray_label_gray":"0088",
            "gray_label_blue2":"0089",

            "blue2_label_black":"0090",
            "blue2_label_blue":"0091",
            "blue2_label_green":"0092",
            "blue2_label_skyblue":"0093",
            "blue2_label_red":"0094",
            "blue2_label_purple":"0095",
            "blue2_label_yellow":"0096",
            "blue2_label_white":"0097",
            "blue2_label_gray":"0098",
            "blue2_label_blue2":"0099",
        }
            return colors

    class output_color():

        def color_print(text,color=0x0007):
            """Set cmd Color and print color is like 0x0002
            
            Sample code:

            import Color_print

            cprint=Color_print.Color.output_color

            cprint.color_print(0002,"test")

            The Sample code output "test" in red letters

            colorに0002を入れると緑色で出力出来ます。textは出力する変数です。

            
            """
            #get now color
            info_ = cutil.console_screen_buffer_info()
            cutil.GetConsoleInfo(cutil.stdout_handle, byref(info_))

            #change console color
            cutil.SetConsoleAttribute(cutil.stdout_handle,color | info_.wAttributes & 0x0070)

            #default print
            print(text)

            #reset color
            cutil.SetConsoleAttribute(cutil.stdout_handle, info_.wAttributes)

            return text

        def setcolor(color=0x0007):
            #get now color
            info_ = cutil.console_screen_buffer_info()
            cutil.GetConsoleInfo(cutil.stdout_handle, byref(info_))

            #change console color
            cutil.SetConsoleAttribute(cutil.stdout_handle,color | info_.wAttributes & 0x0070)

        def setcolor_name(color_name):
            color_list=Color.Color_list.Color()

            color = (((color_list[color_name])))

            color = color.format(len(color)-1)

            color = 0x0+int(color)

            Color.output_color.setcolor(color)

            return color
        
        def resetcolor():

            info_ = cutil.console_screen_buffer_info()
            cutil.GetConsoleInfo(cutil.stdout_handle, byref(info_))

            cutil.SetConsoleAttribute(cutil.stdout_handle, info_.wAttributes)


        def cprint_name(text,color_name="white"):
            """colorにgreenと指定しtextにtestと入れると緑色でtestと出力出来ます。"""
            color_list=Color.Color_list.Color()

            color = (((color_list[color_name])))

            color = color.format(len(color)-1)

            color = 0x0+int(color)

            Color.output_color.color_print(text,color)

            return color