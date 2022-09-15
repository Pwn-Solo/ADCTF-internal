#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "sprites.c"

int loggedin = 0;

typedef struct pokemon{
    void (*fnptr)();
    int8_t hp;
    u_int8_t atk;
    u_int8_t def;
    
} Pokemon;
void reset();

char path[48]= "./info/player-";
Pokemon p = {reset,50,50,50};

void init(){
	setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

void winner(){
    puts("Congratulations , you beat the champion !");
    system("/bin/ls ./info/");
}

void read_input(char *buf, int len){
    int ret = read(0, buf, len);
    if(ret <= 0){
        exit(1);
    }
    buf[len-1] = '\0';
    //enable stack leak 
}

int read_int(){
    char buf[3];
    read_input(buf, 3);
    return atoi(buf);
}

void reset(){
    p.hp = 50;
    p.atk = 50;
    p.def = 50;
}

void view(){
    char buf[40];
    FILE *fp = fopen(path,"r");
    fgets(buf,40,fp);
    printf("Name   :  %s\n",path);
    printf("passwd :  %s\n",buf);
    fclose(fp);

}
void print_stats(Pokemon p, Pokemon op){
    printf("======== YOUR STATS ========\n");
    printf("HP  : %d\n",p.hp);
    printf("ATK : %u\n",p.atk);
    printf("DEF : %u\n",p.def);
    printf("======== ENEMY STATS =======\n");
    printf("HP  : %d\n",op.hp);
    printf("ATK : %u\n",op.atk);
    printf("DEF : %u\n",op.def);
    printf("============================\n");
}

int battle(){

    if (p.hp == 0){
        puts("Please take your pokemon to the pokecentre");
        exit(0);
    }
    Pokemon cpu;
    printf("Who would you like to challenge: \n1.Beginner Trainer\n2.League Champion\n>> ");

    int ch = read_int();

    if (ch == 1) {
        cpu.hp = 50;
        cpu.atk = 50;
        cpu.def = 50;
        cpu.fnptr = print_pokemon;
    }
    else{
        cpu.hp = 127;
        cpu.atk = 127;
        cpu.def = 127;
        cpu.fnptr = print_pokemon;
    }
    
    cpu.fnptr(ch);
    while(p.hp > 0 && cpu.hp > 0){
        
        print_stats(p,cpu);
        printf("1.Tackle\n2.Run Away\nPick your move >> ");

        int c = read_int();  

        if (c == 1){
            int8_t dmg = p.atk -(cpu.def/p.def);
            cpu.hp = cpu.hp - dmg;
            //cpu hp can be made into negative if damage < -128
            //if raised enough p.atk will go from 127 to -128 
            //fckn dumb but i cba 
            printf("dmg dealt -> %d\n",dmg);

            if (cpu.hp <= 0 && ch == 1){
                puts("You Won, your pokemon gained exp");
                print_stats(p,cpu);
                p.hp = 50;
                p.atk++;
                p.def++;
                break;

            }
            else if (cpu.hp <= 0 && ch!= 1){
                print_stats(p,cpu);
                winner();
                break;
            }
        }
        else {
            puts("got away safely");
            break;
        }

        int8_t dmg = cpu.atk -(p.def/cpu.def);
        p.hp = p.hp - dmg;
        printf("dmg taken -> %d\n",dmg);

        if (cpu.hp > 0 && p.hp <= 0){
            puts("Your Pokemon Fainted...");
            p.fnptr();
            break;
        }
    }
}

void login(){
    char name[34];
    char pwd[48];
    p.fnptr();

    puts("Enter your name : ");
    read_input(name,34);    
    
    puts("Add a passphrase : ");
    read_input(pwd,48);

    //bss overflow above fn ptr
    strcat(path,name);

    if(access(path,F_OK)==0){
        printf("Welcome Back %s\n",name);
    }
    else {
        FILE *fp = fopen(path,"w");
        fputs(pwd,fp);
        printf("Welcome , Challenger %s\n",name);
        fclose(fp);
    }
    loggedin = 1;
}

void menu(){

    if (!loggedin){
    puts("============== MENU ==============");
    puts("| 1. Login                       |");
    puts("| 2. Battle                      |");
    puts("| 3. Quit                        |");
    puts("==================================");
    printf(">> ");
    }

    else{
    puts("============== MENU ==============");
    puts("| 1. View Details                |");
    puts("| 2. Battle                      |");
    puts("| 3. Logout                      |");
    puts("==================================");
    printf(">> ");

    }
}

void game_choice(){

    while(1){
        int num;
        menu();
        num = read_int();
        
        if(num == 1)
        {
            if (!loggedin)
                login();
            else
                view();
        }
        else if(num==2)
        {
            if(!loggedin){
                puts("Come back after being id'd");
                continue;
            }
            else
                battle();
        }
        else
        {
            if (!loggedin){
                puts("Bye");
                exit(1);
            }
            else{
                loggedin = 0;
                game_choice();
            }
        }
    }
} 


int main(){

    init();
    print_pokemon(0);
    game_choice();
    
}