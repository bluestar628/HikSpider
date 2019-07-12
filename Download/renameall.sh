#! /bin/bash
function process_rename(){
			rename -v "s/%20/_/g" *
			rename -v "s/%21/!/g" *
			rename -v "s/%22/\"/g" *
			rename -v "s/%23/#/g" *
			rename -v "s/%26/&/g" *
			rename -v "s/%27/'/g" *
			rename -v "s/%28/(/g" *
			rename -v "s/%29/)/g" *
			rename -v "s/%2C/,/g" *
			rename -v "s/%5B/[/g" *
			rename -v "s/%5D/]/g" *
			rename -v "s/%EF%BC%88/(/g" *
			rename -v "s/%EF%BC%89/)/g" *
			rename -v "s/%EF%BC%8C/,/g" *
			rename -v "s/%E3%80%81/、/g" *
}

function read_dir() {
	process_rename
	for file in `ls`
	do
		if [ -d $file ]
		then
			cd $file
			read_dir
			cd ..
		fi
	done
}

read_dir