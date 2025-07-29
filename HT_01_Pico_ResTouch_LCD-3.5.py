from machine import Pin,SPI,PWM
import framebuf
import time
import os
#import gc

LCD_DC   = 8
LCD_CS   = 9
LCD_SCK  = 10
LCD_MOSI = 11
LCD_MISO = 12
LCD_BL   = 13
LCD_RST  = 15
TP_CS    = 16
TP_IRQ   = 17

class LCD_3inch5(framebuf.FrameBuffer):

    def __init__(self):
        self.RED   =   0x07E0
        self.GREEN =   0x001f
        self.BLUE  =   0xf800
        self.WHITE =   0xffff
        self.BLACK =   0x0000
        self.YELLOW =  0x07ef
        self.rotate = 90   # Set the rotation Angle to 0°, 90°, 180° and 270°
        
        self.width = 480
        self.height = 320 #160
            
        self.cs = Pin(LCD_CS,Pin.OUT)
        self.rst = Pin(LCD_RST,Pin.OUT)
        self.dc = Pin(LCD_DC,Pin.OUT)
        
        self.tp_cs =Pin(TP_CS,Pin.OUT)
        self.irq = Pin(TP_IRQ,Pin.IN)
        
        self.cs(1)
        self.dc(1)
        self.rst(1)
        self.tp_cs(1)
        self.spi = SPI(1,6_000_000)
        print(self.spi)  
        self.spi = SPI(1,baudrate=60_000_000,sck=Pin(LCD_SCK),mosi=Pin(LCD_MOSI),miso=Pin(LCD_MISO))
        print(self.spi)      
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        #self.spi.write(bytearray([0X00]))
        self.spi.write(bytearray([buf]))
        self.cs(1)


    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        time.sleep_ms(5)
        self.rst(0)
        time.sleep_ms(10)
        self.rst(1)
        time.sleep_ms(5)
        self.write_cmd(0x21)
        
        self.write_cmd(0xC2)
        self.write_data(0x33)
        
        self.write_cmd(0XC5)
        self.write_data(0x00)
        self.write_data(0x1e)
        self.write_data(0x80)
        
        self.write_cmd(0xB1)
        self.write_data(0xB0)
        
        self.write_cmd(0XE0)
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x04)
        self.write_data(0x0F)
        self.write_data(0x06)
        self.write_data(0x3a)
        self.write_data(0x56)
        self.write_data(0x4d)
        self.write_data(0x03)
        self.write_data(0x0a)
        self.write_data(0x06)
        self.write_data(0x30)
        self.write_data(0x3e)
        self.write_data(0x0f)
        
        self.write_cmd(0XE1)
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x01)
        self.write_data(0x11)
        self.write_data(0x06)
        self.write_data(0x38)
        self.write_data(0x34)
        self.write_data(0x4d)
        self.write_data(0x06)
        self.write_data(0x0d)
        self.write_data(0x0b)
        self.write_data(0x31)
        self.write_data(0x37)
        self.write_data(0x0f)
        
        self.write_cmd(0X3A)
        self.write_data(0x55)
        
        self.write_cmd(0x11)
        time.sleep_ms(5) #120
        self.write_cmd(0x29)
        
        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x62)
        
        self.write_cmd(0x36) # Sets the memory access mode for rotation
        self.write_data(0xe8) #0xe8
            
    def show_up(self):
        
        self.write_cmd(0x2A)
        self.write_data(0x00) # von 0
        self.write_data(0x00)
        self.write_data(0x01) # bis 479
        self.write_data(0xdf)
            
        self.write_cmd(0x2B)
        self.write_data(0x00) # von 0
        self.write_data(0x00)
        self.write_data(0x01) # bis 319
        self.write_data(0x3f)
            
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
    def show_down(self):
        self.write_cmd(0x2A)
        self.write_data(0x00) # von 0
        self.write_data(0x00)
        self.write_data(0x01) # bis 479
        self.write_data(0xdf)
            
        self.write_cmd(0x2B)
        self.write_data(0x00) # von 160
        self.write_data(0xA0)
        self.write_data(0x01) # bis 319
        self.write_data(0x3f)
            
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
    def bl_ctrl(self,duty):
        pwm = PWM(Pin(LCD_BL))
        pwm.freq(1000)
        if(duty>=100):
            pwm.duty_u16(65535)
        else:
            pwm.duty_u16(655*duty)

    def touch_get(self): 
        if self.irq() == 0:
            self.spi = SPI(1,4_000_000,sck=Pin(LCD_SCK),mosi=Pin(LCD_MOSI),miso=Pin(LCD_MISO))
            self.tp_cs(0)
            X_Point = 0
            Y_Point = 0
            for i in range(0,3):
                self.spi.write(bytearray([0XD0]))
                Read_date = self.spi.read(2)
                time.sleep_us(10)
                X_Point=X_Point+(((Read_date[0]<<8)+Read_date[1])>>3)
                
                self.spi.write(bytearray([0X90]))
                Read_date = self.spi.read(2)
                Y_Point=Y_Point+(((Read_date[0]<<8)+Read_date[1])>>3)

            X_Point=X_Point/3
            Y_Point=Y_Point/3
            
            self.tp_cs(1) 
            self.spi = SPI(1,40_000_000,sck=Pin(LCD_SCK),mosi=Pin(LCD_MOSI),miso=Pin(LCD_MISO))
            Result_list = [X_Point,Y_Point]
            #print(Result_list)
            return(Result_list)
        
    def rd_stat(self):
            #self.spi.write(bytearray([0X0C]))
            self.write_cmd(0x0c)
            Read_date = self.spi.read(2)
            time.sleep_us(10)
            print(bin(Read_date[1]))
        
if __name__=='__main__':

    LCD = LCD_3inch5()
    LCD.bl_ctrl(100)
    LCD.fill(LCD.BLACK)
    LCD.show_up()
    #LCD.fill(LCD.BLACK)
    #LCD.show_down()



    #color BRG     
    LCD.fill(LCD.BLACK)
    LCD.fill_rect(40,5,400,30,LCD.RED)
    LCD.text("Raspberry Pi Pico",170,17,LCD.WHITE)
    display_color = 1 #0x001F
    LCD.text("3.5\" IPS LCD TEST",170,57,LCD.WHITE)
    #for i in range(0,12):
    for i in range(0,15):
        #LCD.fill_rect(i+30+60,100,30,30,(display_color))
        LCD.fill_rect(i*30+50,90,30,20,i)
        LCD.fill_rect(i*30+50,110,30,20,i<<5)
        LCD.fill_rect(i*30+50,130,30,20,i<<10)
        #display_color = display_color << 1
        display_color = display_color +1
            
        #LCD.hline(10,60,460,LCD.GREEN)
        #LCD.hline(10,61,460,LCD.GREEN)
        #LCD.rect(10,64,50,20,LCD.BLACK)
        #LCD.ellipse(240,70,15,30,LCD.RED,True)
    LCD.show_up()
        
    while True:      
        get = LCD.touch_get()
        if get != None: 
            X_Point = 480-int((get[1]-4390)*480/3655)
            #6print("X_Point= ",X_Point,end="")
            if(X_Point>480):
                X_Point = 480
            elif X_Point<0:
                X_Point = 0
            Y_Point = int((get[0]-4416)*320/3270)
            if (Y_Point>319):
                Y_Point = 319
            elif(Y_Point<0):
                Y_Point = 0
            print(" XY_Point= ",X_Point,Y_Point)
# When the rotation is 90°, remove the comment below, and the touch rotation at 270° can be annotated
# 90° touch rotation is enabled by default
            if (Y_Point>220): #120
                #LCD.fill(LCD.BLACK)
                if(X_Point>380):
                    LCD.fill_rect(370,200,120,119,LCD.GREEN)
                    LCD.text("Button3",400,250,LCD.WHITE)
                elif(X_Point>260):
                    LCD.fill_rect(240,200,120,119,LCD.YELLOW)
                    LCD.text("Knopf2",270,250,LCD.WHITE)
                elif(X_Point>140):
                    LCD.fill_rect(120,200,120,119,LCD.RED)
                    LCD.text("Knopf1",140,250,LCD.WHITE)          
                else:               
                    LCD.fill_rect(0,200,120,119,LCD.BLUE)
                    LCD.text("Button0",10,250,LCD.WHITE)
                    #print('xpoint=',X_Point,"Y_Point=",Y_Point)
        else :
           LCD.fill_rect(0,200,480,119,LCD.BLACK)
           LCD.text("Button0",10,250,LCD.WHITE)
           LCD.text("Knopf1",140,250,LCD.WHITE)
           LCD.text("Knopf2",270,250,LCD.WHITE)
           LCD.text("Button3",400,250,LCD.WHITE)
        
        #LCD.rd_stat()
        LCD.show_up()
            #print(gc.mem_free(),end='\n')
        time.sleep(0.2)
               