import torch.nn as nn
import torch
from torch import autograd


class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(DoubleConv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),

            nn.GroupNorm(out_ch // 32, out_ch), 
            nn.ReLU(inplace=True),

            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            # nn.BatchNorm2d(out_ch),
            nn.GroupNorm(out_ch // 32,out_ch), 
            nn.ReLU(inplace=True)
        )

    def forward(self, input):
        return self.conv(input)
###############################################################################################################################
class ResDoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(DoubleConv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),

            nn.GroupNorm(out_ch // 32, out_ch), 
            nn.ReLU(inplace=True),

            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            # nn.BatchNorm2d(out_ch),
            nn.GroupNorm(out_ch // 32,out_ch), 
            nn.ReLU(inplace=True)
        )

    def forward(self, input):
        return self.conv(input)+input
###############################################################################################################################
class Unet4(nn.Module):
    def __init__(self, in_ch, out_ch, f_num):
        super(Unet4, self).__init__()
        self.conv1 = DoubleConv(in_ch, f_num)
        self.pool1 = nn.MaxPool2d(2)
        self.conv2 = DoubleConv(f_num, f_num*2)
        self.pool2 = nn.MaxPool2d(2)
        self.conv3 = DoubleConv(f_num*2, f_num*2*2)
        self.pool3 = nn.MaxPool2d(2)
        self.conv4 = DoubleConv(f_num*2*2, f_num*2*2*2)
        self.pool4 = nn.MaxPool2d(2)
        self.conv5 = DoubleConv(f_num*2*2*2, f_num*2*2*2*2)

        self.res_conv1 = ResDoubleConv(f_num*2*2*2*2, f_num*2*2*2*2)
        self.res_conv2 = ResDoubleConv(f_num*2*2*2*2, f_num*2*2*2*2)
        self.res_conv3 = ResDoubleConv(f_num*2*2*2*2, f_num*2*2*2*2)
        self.res_conv4 = ResDoubleConv(f_num*2*2*2*2, f_num*2*2*2*2)
        self.res_conv5 = ResDoubleConv(f_num*2*2*2*2, f_num*2*2*2*2)
        self.res_conv6 = ResDoubleConv(f_num*2*2*2*2, f_num*2*2*2*2)
        self.res_conv7 = ResDoubleConv(f_num*2*2*2*2, f_num*2*2*2*2)
        self.res_conv8 = ResDoubleConv(f_num*2*2*2*2, f_num*2*2*2*2)
        self.res_conv9 = ResDoubleConv(f_num*2*2*2*2, f_num*2*2*2*2)

        self.up6 = nn.ConvTranspose2d(f_num*2*2*2*2, f_num*2*2*2, 2, stride=2)
        self.conv6 = DoubleConv(f_num*2*2*2*2, f_num*2*2*2)
        self.up7 = nn.ConvTranspose2d(f_num*2*2*2, f_num*2*2, 2, stride=2)
        self.conv7 = DoubleConv(f_num*2*2*2, f_num*2*2)
        self.up8 = nn.ConvTranspose2d(f_num*2*2, f_num*2, 2, stride=2)
        self.conv8 = DoubleConv(f_num*2*2, f_num*2)
        self.up9 = nn.ConvTranspose2d(f_num*2, f_num, 2, stride=2)
        self.conv9 = DoubleConv(f_num*2, f_num)
        self.conv10 = nn.Conv2d(f_num, out_ch, 1)

    def forward(self, x):
        c1 = self.conv1(x)
        p1 = self.pool1(c1)
        c2 = self.conv2(p1)
        p2 = self.pool2(c2)
        c3 = self.conv3(p2)
        p3 = self.pool3(c3)
        c4 = self.conv4(p3)
        p4 = self.pool4(c4)
        c5 = self.conv5(p4)
        up_6 = self.up6(c5)

        up_6 = self.res_conv1(up_6)
        up_6 = self.res_conv2(up_6)
        up_6 = self.res_conv3(up_6)
        up_6 = self.res_conv4(up_6)
        up_6 = self.res_conv5(up_6)
        up_6 = self.res_conv6(up_6)
        up_6 = self.res_conv7(up_6)
        up_6 = self.res_conv8(up_6)
        up_6 = self.res_conv9(up_6)

        merge6 = torch.cat([up_6, c4], dim=1)
        c6 = self.conv6(merge6)
        up_7 = self.up7(c6)
        merge7 = torch.cat([up_7, c3], dim=1)
        c7 = self.conv7(merge7)
        up_8 = self.up8(c7)
        merge8 = torch.cat([up_8, c2], dim=1)
        c8 = self.conv8(merge8)
        up_9 = self.up9(c8)
        merge9 = torch.cat([up_9, c1], dim=1)
        c9 = self.conv9(merge9)
        c10 = self.conv10(c9)
        # out = nn.Sigmoid()(c10)
        out = c10
        return out
        # return c10
################################################################################################################################
class Unet4_res(nn.Module):
    def __init__(self, in_ch, out_ch, f_num):
        super(Unet4, self).__init__()
        self.conv1 = DoubleConv(in_ch, f_num)
        self.pool1 = nn.MaxPool2d(2)
        self.conv2 = DoubleConv(f_num, f_num*2)
        self.pool2 = nn.MaxPool2d(2)
        self.conv3 = DoubleConv(f_num*2, f_num*2*2)
        self.pool3 = nn.MaxPool2d(2)
        self.conv4 = DoubleConv(f_num*2*2, f_num*2*2*2)
        self.pool4 = nn.MaxPool2d(2)
        self.conv5 = DoubleConv(f_num*2*2*2, f_num*2*2*2*2)

        self.up6 = nn.ConvTranspose2d(f_num*2*2*2*2, f_num*2*2*2, 2, stride=2)
        self.conv6 = DoubleConv(f_num*2*2*2*2, f_num*2*2*2)
        self.up7 = nn.ConvTranspose2d(f_num*2*2*2, f_num*2*2, 2, stride=2)
        self.conv7 = DoubleConv(f_num*2*2*2, f_num*2*2)
        self.up8 = nn.ConvTranspose2d(f_num*2*2, f_num*2, 2, stride=2)
        self.conv8 = DoubleConv(f_num*2*2, f_num*2)
        self.up9 = nn.ConvTranspose2d(f_num*2, f_num, 2, stride=2)
        self.conv9 = DoubleConv(f_num*2, f_num)
        self.conv10 = nn.Conv2d(f_num, out_ch, 1)

    def forward(self, x):
        c1 = self.conv1(x)
        p1 = self.pool1(c1)
        c2 = self.conv2(p1)
        p2 = self.pool2(c2)
        c3 = self.conv3(p2)
        p3 = self.pool3(c3)
        c4 = self.conv4(p3)
        p4 = self.pool4(c4)
        c5 = self.conv5(p4)
        up_6 = self.up6(c5)
        merge6 = torch.cat([up_6, c4], dim=1)
        c6 = self.conv6(merge6)
        up_7 = self.up7(c6)
        merge7 = torch.cat([up_7, c3], dim=1)
        c7 = self.conv7(merge7)
        up_8 = self.up8(c7)
        merge8 = torch.cat([up_8, c2], dim=1)
        c8 = self.conv8(merge8)
        up_9 = self.up9(c8)
        merge9 = torch.cat([up_9, c1], dim=1)
        c9 = self.conv9(merge9)
        c10 = self.conv10(c9)
        # out = nn.Sigmoid()(c10)
        out = c10
        return out

#################################################################################################################################
class Unet3(nn.Module):
    def __init__(self, in_ch, out_ch, f_num):
        super(Unet3, self).__init__()
        self.conv1 = DoubleConv(in_ch, f_num)
        self.pool1 = nn.MaxPool2d(2)
        self.conv2 = DoubleConv(f_num, f_num*2)
        self.pool2 = nn.MaxPool2d(2)
        self.conv3 = DoubleConv(f_num*2, f_num*2*2)
        self.pool3 = nn.MaxPool2d(2)
        self.conv4 = DoubleConv(f_num*2*2, f_num*2*2*2)

        self.up7 = nn.ConvTranspose2d(f_num*2*2*2, f_num*2*2, 2, stride=2)
        self.conv7 = DoubleConv(f_num*2*2*2, f_num*2*2)
        self.up8 = nn.ConvTranspose2d(f_num*2*2, f_num*2, 2, stride=2)
        self.conv8 = DoubleConv(f_num*2*2, f_num*2)
        self.up9 = nn.ConvTranspose2d(f_num*2, f_num, 2, stride=2)
        self.conv9 = DoubleConv(f_num*2, f_num)
        self.conv10 = nn.Conv2d(f_num, out_ch, 1)

    def forward(self, x):
        c1 = self.conv1(x)
        p1 = self.pool1(c1)
        c2 = self.conv2(p1)
        p2 = self.pool2(c2)
        c3 = self.conv3(p2)
        p3 = self.pool3(c3)
        c4 = self.conv4(p3)
        up_7 = self.up7(c4)
        merge7 = torch.cat([up_7, c3], dim=1)
        c7 = self.conv7(merge7)
        up_8 = self.up8(c7)
        merge8 = torch.cat([up_8, c2], dim=1)
        c8 = self.conv8(merge8)
        up_9 = self.up9(c8)
        merge9 = torch.cat([up_9, c1], dim=1)
        c9 = self.conv9(merge9)
        c10 = self.conv10(c9)
        # out = nn.Sigmoid()(c10)
        out = c10
        return out
        # return c10
###############################################################################################################################
class EndBlock(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(EndBlock, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.ReLU(inplace=True)
        )
    def forward(self, x):
        out = self.conv(x)
        return out
