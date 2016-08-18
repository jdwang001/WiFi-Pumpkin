from re import search
import Modules as GUIs
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Core.Utils import Refactor
from Core.widgets.PluginsSettings import BDFProxy_ConfigObject
"""
Description:
    This program is a Core for wifi-pumpkin.py. file which includes functionality
    for load plugins mitm attack and phishing module.

Copyright:
    Copyright (C) 2015-2016 Marcos Nesster P0cl4bs Team
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

class PopUpPlugins(QWidget):
    ''' this module control all plugins to MITM attack'''
    def __init__(self,FSettings):
        QWidget.__init__(self)
        self.FSettings = FSettings
        self.layout = QVBoxLayout()
        self.layoutform = QFormLayout()
        self.layoutproxy = QFormLayout()
        self.GroupPlugins = QGroupBox()
        self.GroupPluginsProxy = QGroupBox()
        self.GroupPlugins.setTitle(':: Plugins ::')
        self.GroupPluginsProxy.setTitle(':: Proxy ::')
        self.GroupPluginsProxy.setLayout(self.layoutproxy)
        self.GroupPlugins.setLayout(self.layoutform)
        self.check_netcreds     = QCheckBox('net-creds ')
        self.check_dns2proy     = QRadioButton('sslstrip+/dns2proxy')
        self.check_sergioProxy  = QRadioButton('sslstrip/sergio-proxy')
        self.check_bdfproxy     = QRadioButton('BDFProxy-ng')
        self.check_noproxy      = QRadioButton('No Proxy')

        self.btnBDFSettings    = QPushButton('Config')
        self.btnBDFSettings.setIcon(QIcon('Icons/config.png'))
        self.btnBDFSettings.clicked.connect(self.ConfigOBJBDFproxy)

        self.proxyGroup = QButtonGroup()
        self.proxyGroup.addButton(self.check_dns2proy)
        self.proxyGroup.addButton(self.check_sergioProxy)
        self.proxyGroup.addButton(self.check_noproxy)
        self.proxyGroup.addButton(self.check_bdfproxy)

        self.check_netcreds.clicked.connect(self.checkBoxNecreds)
        self.check_dns2proy.clicked.connect(self.checkGeneralOptions)
        self.check_sergioProxy.clicked.connect(self.checkGeneralOptions)
        self.check_bdfproxy.clicked.connect(self.checkGeneralOptions)
        self.check_noproxy.clicked.connect(self.checkGeneralOptions)

        self.layoutform.addRow(self.check_netcreds)
        self.layoutproxy.addRow(self.check_dns2proy)
        self.layoutproxy.addRow(self.check_sergioProxy)
        self.layoutproxy.addRow(self.check_bdfproxy,self.btnBDFSettings)
        self.layoutproxy.addRow(self.check_noproxy)
        self.layout.addWidget(self.GroupPlugins)
        self.layout.addWidget(self.GroupPluginsProxy)
        self.setLayout(self.layout)

    # control checkbox plugins
    def checkGeneralOptions(self):
        self.unset_Rules('dns2proxy')
        self.unset_Rules('sslstrip')
        self.unset_Rules('bdfproxy')
        if self.check_sergioProxy.isChecked():
            self.FSettings.Settings.set_setting('plugins','sergioproxy_plugin',True)
            self.FSettings.Settings.set_setting('plugins','dns2proxy_plugin',False)
            self.FSettings.Settings.set_setting('plugins','noproxy',False)
            self.FSettings.Settings.set_setting('plugins','bdfproxy_plugin',False)
            self.set_sslStripRule()
        elif self.check_dns2proy.isChecked():
            self.FSettings.Settings.set_setting('plugins','dns2proxy_plugin',True)
            self.FSettings.Settings.set_setting('plugins','sergioproxy_plugin',False)
            self.FSettings.Settings.set_setting('plugins','noproxy',False)
            self.FSettings.Settings.set_setting('plugins','bdfproxy_plugin',False)
            self.set_sslStripRule()
            self.set_Dns2proxyRule()
        elif self.check_bdfproxy.isChecked():
            self.FSettings.Settings.set_setting('plugins','bdfproxy_plugin',True)
            self.FSettings.Settings.set_setting('plugins','dns2proxy_plugin',False)
            self.FSettings.Settings.set_setting('plugins','sergioproxy_plugin',False)
            self.FSettings.Settings.set_setting('plugins','noproxy',False)
            self.unset_Rules('dns2proxy')
            self.unset_Rules('sslstrip')
            self.set_BDFproxyRule()
        elif self.check_noproxy.isChecked():
            self.FSettings.Settings.set_setting('plugins','dns2proxy_plugin',False)
            self.FSettings.Settings.set_setting('plugins','sergioproxy_plugin',False)
            self.FSettings.Settings.set_setting('plugins','bdfproxy_plugin',False)
            self.FSettings.Settings.set_setting('plugins','noproxy',True)
            self.unset_Rules('dns2proxy')
            self.unset_Rules('sslstrip')
            self.unset_Rules('bdfproxy')

    def ConfigOBJBDFproxy(self):
        self.SettingsBDFProxy  = BDFProxy_ConfigObject()
        self.SettingsBDFProxy.show()

    def checkBoxNecreds(self):
        if self.check_netcreds.isChecked():
            self.FSettings.Settings.set_setting('plugins','netcreds_plugin',True)
        else:
            self.FSettings.Settings.set_setting('plugins','netcreds_plugin',False)

    def optionsRules(self,type):
        search = {
        'sslstrip': str('iptables -t nat -A PREROUTING -p tcp'+
        ' --destination-port 80 -j REDIRECT --to-port '+self.FSettings.redirectport.text()),
        'dns2proxy':str('iptables -t nat -A PREROUTING -p udp --destination-port 53 -j REDIRECT --to-port 53'),
        'bdfproxy':str('iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port '+
        str(self.FSettings.bdfProxy_port.value()))}
        return search[type]

    # set rules to sslstrip
    def set_sslStripRule(self):
        items = []
        for index in xrange(self.FSettings.ListRules.count()):
            items.append(str(self.FSettings.ListRules.item(index).text()))
        if self.optionsRules('sslstrip') in items:
            return
        item = QListWidgetItem()
        item.setText(self.optionsRules('sslstrip'))
        item.setSizeHint(QSize(30,30))
        self.FSettings.ListRules.addItem(item)

    # set redirect port rules dns2proy
    def set_Dns2proxyRule(self):
        item = QListWidgetItem()
        item.setText(self.optionsRules('dns2proxy'))
        item.setSizeHint(QSize(30,30))
        self.FSettings.ListRules.addItem(item)

    # set redirect port rules bdfproxy
    def set_BDFproxyRule(self):
        items = []
        for index in xrange(self.FSettings.ListRules.count()):
            items.append(str(self.FSettings.ListRules.item(index).text()))
        if self.optionsRules('bdfproxy') in items:
            return
        item = QListWidgetItem()
        item.setText(self.optionsRules('bdfproxy'))
        item.setSizeHint(QSize(30,30))
        self.FSettings.ListRules.addItem(item)

    def unset_Rules(self,type):
        items = []
        for index in xrange(self.FSettings.ListRules.count()):
            items.append(str(self.FSettings.ListRules.item(index).text()))
        for position,line in enumerate(items):
            if self.optionsRules(type) == line:
                self.FSettings.ListRules.takeItem(position)


class PopUpServer(QWidget):
    ''' this module fast access to phishing-manager'''
    def __init__(self,FSettings):
        QWidget.__init__(self)
        self.FSettings  = FSettings
        self.Ftemplates = GUIs.frm_PhishingManager()
        self.layout     = QVBoxLayout()
        self.FormLayout = QFormLayout()
        self.GridForm   = QGridLayout()
        self.Status     = QStatusBar()
        self.StatusLabel= QLabel(self)
        self.Status.addWidget(QLabel('Status::'))
        self.Status.addWidget(self.StatusLabel)
        self.GroupBox           = QGroupBox()
        self.GroupBox.setTitle('::Server-HTTP::')
        self.GroupBox.setLayout(self.FormLayout)
        self.btntemplates       = QPushButton('Phishing M.')
        self.btnStopServer      = QPushButton('Stop Server')
        self.btnRefresh         = QPushButton('ReFresh')
        self.txt_IP             = QLineEdit(self)
        self.ComboIface         = QComboBox(self)
        self.txt_IP.setVisible(False)
        self.StatusServer(False)
        #icons
        self.btntemplates.setIcon(QIcon('Icons/page.png'))
        self.btnStopServer.setIcon(QIcon('Icons/close.png'))
        self.btnRefresh.setIcon(QIcon('Icons/refresh.png'))

        #conects
        self.refrash_interface()
        self.btntemplates.clicked.connect(self.show_template_dialog)
        self.btnStopServer.clicked.connect(self.StopLocalServer)
        self.btnRefresh.clicked.connect(self.refrash_interface)
        self.connect(self.ComboIface, SIGNAL('currentIndexChanged(QString)'), self.discoveryIface)

        #layout
        self.GridForm.addWidget(self.ComboIface,0,1)
        self.GridForm.addWidget(self.btnRefresh,0,2)
        self.GridForm.addWidget(self.btntemplates,1,1)
        self.GridForm.addWidget(self.btnStopServer,1,2)
        self.FormLayout.addRow(self.GridForm)
        self.FormLayout.addWidget(self.Status)
        self.layout.addWidget(self.GroupBox)
        self.setLayout(self.layout)


    def emit_template(self,log):
        if log == 'started':
            self.StatusServer(True)

    def StopLocalServer(self):
        self.StatusServer(False)
        self.Ftemplates.killThread()

    def StatusServer(self,server):
        if server:
            self.StatusLabel.setText('[ ON ]')
            self.StatusLabel.setStyleSheet('QLabel {  color : green; }')
        elif not server:
            self.StatusLabel.setText('[ OFF ]')
            self.StatusLabel.setStyleSheet('QLabel {  color : red; }')

    def refrash_interface(self):
        self.ComboIface.clear()
        n = Refactor.get_interfaces()['all']
        for i,j in enumerate(n):
            if search('at',j) or search('wl',j):
                self.ComboIface.addItem(n[i])
                self.discoveryIface()

    def discoveryIface(self):
        iface = str(self.ComboIface.currentText())
        ip = Refactor.get_Ipaddr(iface)
        self.txt_IP.setText(ip)

    def show_template_dialog(self):
        self.connect(self.Ftemplates,SIGNAL('Activated ( QString ) '), self.emit_template)
        self.Ftemplates.txt_redirect.setText(self.txt_IP.text())
        self.Ftemplates.show()
