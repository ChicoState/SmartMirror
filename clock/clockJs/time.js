function showTime()
{
	var date = new Date();
	var hours = date.getHours();
	var minutes = date.getMinutes();
	var seconds = date.getSeconds();
	var sessionID = "AM"


	if(hours == 0)
	{
		hours = 12;
	}

	if(hours > 12)
	{
		hours -= 12;
		sessionID = "PM"
	}

	hours = (hours < 10) ? "0" + hours : hours;
	minutes = (minutes < 10) ? "0" + minutes : minutes;
	//seconds = (seconds < 10) ? "0" + seconds : seconds;

	//var time = hours + ":" + minutes + ":" + seconds + " " + sessionID;
	var time = hours + ":" + minutes + " " + sessionID;

	document.getElementById("MyClockDisplay").innerText = time;
	document.getElementById("MyClockDisplay").textContent = time;

	//Called every millisecond
	setTimeout(showTime, 1000);
}

showTime()
