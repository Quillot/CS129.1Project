map1 = function(){
	var key = {year: this.year, genre: this.genre}
	emit({year: this.year,
		genre: this.genre}, 1)
}

reduce1 = function(key, values){
	var count = 0;
	for(var i = 0; i < values.length; i++){
		count += values[i];
	}
	return count;
}

result1 = db.runCommand({
	mapReduce: 'songs',
	map: map1,
	reduce: reduce1,
	out: 'songs.answer1'
});


map2 = function(){
	emit(this._id.genre, this.value)
}

reduce2 = function(key, values){
	var count = 0;
	for(var i = 0; i < values.length; i++){
		count += values[i];
	}
	return count;
}

result2 = db.runCommand({
	mapReduce: 'songs.answer1',
	map: map2,
	reduce: reduce2,
	out: 'songs.answer2'
});

map3 = function(){
	var key = {year: this.year, genre: this.genre, word: this.word}
	emit(key, this.word_count)
}

reduce3 = function(key, values){
	var count = 0;
	for(var i = 0; i < values.length; i++){
		count += values[i];
	}
	return count;
}

result3 = db.runCommand({
	mapReduce: 'songs',
	map: map3,
	reduce: reduce3,
	out: 'songs.answer3'
});

map4 = function(){
	emit(this._id.word, this.value)
}
reduce4 = function(key, values){
	var count = 0;
	for(var i = 0; i < values.length; i++){
		count += values[i];
	}
	return count;
}

result4 = db.runCommand({
	mapReduce: 'songs.answer3',
	map: map4,
	reduce: reduce4,
	out: 'songs.answer4'
});

map5 = function(){
	var key = {year: this.year, word: this.word}
	emit(key, 1)
}

reduce5 = function(key, values){
	var count = 0;
	for(var i = 0; i < values.length; i++){
		count += values[i];
	}
	return count;
}

result5 = db.runCommand({
	mapReduce: 'songs',
	map: map5,
	reduce: reduce5,
	out: 'songs.answer5'
});