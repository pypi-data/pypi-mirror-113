<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainUi</class>
 <widget class="QDialog" name="MainUi">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>330</width>
    <height>286</height>
   </rect>
  </property>
  <property name="palette">
   <palette>
    <active/>
    <inactive/>
    <disabled/>
   </palette>
  </property>
  <property name="font">
   <font>
    <family>Arimo for Powerline</family>
    <bold>true</bold>
   </font>
  </property>
  <property name="windowTitle">
   <string>Django Maker</string>
  </property>
  <property name="sizeGripEnabled">
   <bool>true</bool>
  </property>
  <property name="modal">
   <bool>true</bool>
  </property>
  <layout class="QFormLayout" name="formDjango">
   <item row="2" column="0">
    <widget class="QLabel" name="nomeAPPLabel">
     <property name="text">
      <string>Nome APP</string>
     </property>
    </widget>
   </item>
   <item row="2" column="1">
    <widget class="QLineEdit" name="nome_input"/>
   </item>
   <item row="3" column="0">
    <widget class="QLabel" name="portaAPPLabel">
     <property name="text">
      <string>Porta APP</string>
     </property>
    </widget>
   </item>
   <item row="3" column="1">
    <widget class="QLineEdit" name="porta_input"/>
   </item>
   <item row="4" column="0">
    <widget class="QLabel" name="bancoDeDadosPortaLabel">
     <property name="text">
      <string>Banco de Dados Porta</string>
     </property>
    </widget>
   </item>
   <item row="4" column="1">
    <widget class="QLineEdit" name="bd_porta_input"/>
   </item>
   <item row="5" column="0">
    <widget class="QLabel" name="pythonVersOLabel">
     <property name="text">
      <string>Python Versão</string>
     </property>
    </widget>
   </item>
   <item row="5" column="1">
    <widget class="QLineEdit" name="python_input"/>
   </item>
   <item row="6" column="0">
    <widget class="QLabel" name="postgresUsuRioLabel">
     <property name="text">
      <string>Postgres Usuário</string>
     </property>
    </widget>
   </item>
   <item row="6" column="1">
    <widget class="QLineEdit" name="user_input"/>
   </item>
   <item row="7" column="0">
    <widget class="QLabel" name="postgresSenhaLabel">
     <property name="text">
      <string>Postgres Senha</string>
     </property>
    </widget>
   </item>
   <item row="7" column="1">
    <widget class="QLineEdit" name="password_input"/>
   </item>
   <item row="8" column="0">
    <widget class="QLabel" name="postgresHostLabel">
     <property name="text">
      <string>Postgres Host</string>
     </property>
    </widget>
   </item>
   <item row="8" column="1">
    <widget class="QLineEdit" name="bd_input"/>
   </item>
   <item row="9" column="0">
    <widget class="QLabel" name="caminhoDoAPPLabel">
     <property name="text">
      <string>Caminho do APP</string>
     </property>
    </widget>
   </item>
   <item row="9" column="1">
    <widget class="QLineEdit" name="path_input"/>
   </item>
   <item row="10" column="1">
    <widget class="QDialogButtonBox" name="buttonBox">
     <property name="orientation">
      <enum>Qt::Horizontal</enum>
     </property>
     <property name="standardButtons">
      <set>QDialogButtonBox::Cancel|QDialogButtonBox::Ok</set>
     </property>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections>
  <connection>
   <sender>buttonBox</sender>
   <signal>accepted()</signal>
   <receiver>MainUi</receiver>
   <slot>accept()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>248</x>
     <y>254</y>
    </hint>
    <hint type="destinationlabel">
     <x>157</x>
     <y>274</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>buttonBox</sender>
   <signal>rejected()</signal>
   <receiver>MainUi</receiver>
   <slot>reject()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>316</x>
     <y>260</y>
    </hint>
    <hint type="destinationlabel">
     <x>286</x>
     <y>274</y>
    </hint>
   </hints>
  </connection>
 </connections>
</ui>
