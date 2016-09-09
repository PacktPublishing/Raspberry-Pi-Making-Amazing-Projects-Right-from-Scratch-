<?php
$CONFIG_PATH = '/etc/pi-alarm/alarm.cfg';

// == PAGE POST-BACK HANDLER ==========
if(isset($_POST['submit'])) {
	//update submitted settings
	$isPostBack = 1;
	
	//update master arm/disarm switch
	if (isset($_POST['swMaster'])) {$v='1';} else {$v='0';}	
	//this will call a bash script to update the arm config file 
	exec('sudo /etc/pi-alarm/update-alarm-setting.sh "SYSTEM_ARMED" "'.$v.'"');
	
	//update each zone switch status
	for($x = 0; $x < $_POST['numZones']; $x++) {
		if (isset($_POST['swZone'.$x])) {$v='1';} else {$v='0';}
		exec('sudo /etc/pi-alarm/update-alarm-setting.sh "ZONE_ENABLE_"'.$x.' "'.$v.'"');
	}
} else {
	$isPostBack = 0;
}
// ====================================

// Load alarm settings from config file
exec('sudo /bin/cat '.$CONFIG_PATH ,$alarmConfig);
foreach($alarmConfig as $a) {
  if ($a != '') {
    if($a[0] != "#") {
      $arrLine = explode("=",$a);
      $configSettings[$arrLine[0]]=trim($arrLine[1],'"');
    }
  }
}

// == MAIN HTML =======================
echo '
<html lang="en-gb">
<head>
<meta charset="utf-8">
<meta http-equiv="cleartype" content="on" />
<meta name="HandheldFriendly" content="True" />
<meta name="MobileOptimized" content="320"/>
<meta name="viewport" content="user-scalable=no,width=device-width,initial-scale=1.0" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black" />
<link rel="stylesheet" href="alarm-panel.css" />
</head>
<body>
<div id="container">
<div id="header"><h1>Alarm Control Panel</h1></div>
<form action="#" method="post">
';

if ($isPostBack == 1) {
	// display update confirmation
	echo '<p style="color:#00aa00;text-align:center">The system has been updated</p>';
}

// Master On/Off Switch
echo '<div id="masterControl" class="masterControl"><div class="zoneLabel">Master Arm / Disarm</div>';
echo '<div class="masterswitch"><input type="checkbox" name="swMaster" class="masterswitch-checkbox" id="swMaster"';
// if zone is enabled then it will be displayed as ARMED
if ($configSettings['SYSTEM_ARMED'] == 1) {echo ' checked';}
echo '><label class="masterswitch-label" for="swMaster"><span class="masterswitch-inner"></span>';
echo '<span class="masterswitch-switch"></span></label></div></div>';

// Write out zone panel for each of the zones
for($x = 0; $x < $configSettings['NUM_ZONES']; $x++) {
	$iZoneNum = $x + 1; //the zone number
	echo '<div class="zoneControl"><div class="zoneLabel';
	
	// if zone is triggered then flash label red
	if ($configSettings['ZONE_STATUS_'.$iZoneNum] == 1) {echo ' animated flash';}	
	
	echo '">'.$configSettings['ZONE_LABEL_'.$iZoneNum];
	echo '</div><div class="onoffswitch"><input type="checkbox" name="swZone'.$iZoneNum.'" class="onoffswitch-checkbox" id="swZone'.$iZoneNum.'"';
	
	// if zone is enabled then it will be displayed as ON
	if ($configSettings['ZONE_ENABLE_'.$iZoneNum] == 1) {echo ' checked';}
	
	echo '><label class="onoffswitch-label" for="swZone'.$iZoneNum.'">';
	echo '<span class="onoffswitch-inner"></span><span class="onoffswitch-switch"></span></label></div></div>';
}

//store number of zones for post-back
echo '<input type="hidden" name="numZones" value="'.$x.'"/>';
echo '<br/><br/><input type="submit" name="submit" value="Update System" /></form>';
echo '</div></body></html>';

?>