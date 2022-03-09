# CS337 - OPERATING SYSTEMS- Project 4 
#### By: Matthew Bass


**Project Abstract:**
    
In this project I am familiarizing myself with how the xv6 operating system works (a real OS!). This is to serve as great practice for me in implementing real Operating Systems in C and  working Makefiles. In this project I will, add atributes to preexisting objects in the OS such a the priority attribute to procs, implement multiple system calls such as nice (which is used to change a processes priortiy) and finaly implement Priority-based Round-robin Scheduling.


### PREREQUISITES:
    C

 - Mac:
    - qemu x86_64-elf-gcc

- Windows:
    - nasm build-essential qemu gdb


<br>

---


### To Run:

Mac:

    cd xv6-proj4
    export TOOLPREFIX=x86_64-elf-
    export QEMU=qemu-system-x86_64
    make
    make qemu-nox




Windows:

    cd xv6-proj4
    make
    make qemu-nox


**Make sure not to compile with `-Werror` (means "turn all warnings into fatal errors") If on Mac**

**If on windows add “-display none”
to the end of the following line: QEMUOPTS = -hdb fs.img xv6.img -smp \$(CPUS)
-m 512 \$(QEMUEXTRA)**

Once you run the following lines in the terminal you will presented with a shell for xv6


<br>

---

### Process Status System Call:

The `ps` command is used to list the currently running
processes and their PIDs along with the processes priority and state. 

To implement this was very simple as I just followed the code provided in the [project notes](https://github.com/mattjax16/CS337-Operating-Systems/blob/925bae9d1ede96112102ce7e467705be00c7f6e8/Projects/Proj4/Project%204_%20%20Priority-based%20Scheduling%20in%20Xv6.pdf)

Below is a photo of the ps function working in Xv6:

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/2ef2c014bc6f321cef38339bc2519b9a793535cf/Projects/Proj4/Pics/working_ps.png" alt="Process Status Working" />



<br>

---

### Write the Multiprocessing file foo.c:

The goal here was to create a program that uses fork to create multiple CPU-bound processes (called `foo`).  This will help us test our scheduler and system calls.  The code for foo.c is provided

To implement this was very simple as I just followed the code provided in the [project notes](https://github.com/mattjax16/CS337-Operating-Systems/blob/925bae9d1ede96112102ce7e467705be00c7f6e8/Projects/Proj4/Project%204_%20%20Priority-based%20Scheduling%20in%20Xv6.pdf)

Below is a photo of the foo function working in Xv6 (we can see it does show up and a forked process with a parent and child process):

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/2ef2c014bc6f321cef38339bc2519b9a793535cf/Projects/Proj4/Pics/foo_working.png" alt="Foo Working" />




<br>

---

### Adding Priority to Xv6 Processes :

The goal here was add the priority attribute to the processes which we can see was added in the photos above. 

Again to implement this was very simple as I just followed the code provided in the [project notes](https://github.com/mattjax16/CS337-Operating-Systems/blob/925bae9d1ede96112102ce7e467705be00c7f6e8/Projects/Proj4/Project%204_%20%20Priority-based%20Scheduling%20in%20Xv6.pdf)



<br>

---

### Adding the Nice System call:

Here we are ready to add the `nice` system call!  The `nice` system call is responsible for changing the priority of a process while it is running using its process ID.

To implement this was very simple as I just followed the code provided in the [project notes](https://github.com/mattjax16/CS337-Operating-Systems/blob/925bae9d1ede96112102ce7e467705be00c7f6e8/Projects/Proj4/Project%204_%20%20Priority-based%20Scheduling%20in%20Xv6.pdf)

Below is a photo of the nice system working in Xv6 (we can see the original priority of the foo child process, pid 4, was 2 and now after the nice call it is 20):

<img src="https://github.com/mattjax16/CS337-Operating-Systems/blob/2ef2c014bc6f321cef38339bc2519b9a793535cf/Projects/Proj4/Pics/nice_working.png" alt="Nice Working" />




<br>

---

### Resources:
- [Dr. Al Madi](https://www.cs.colby.edu/nsalmadi/)
- [Dr. Al Madi Xv6 notes](https://github.com/mattjax16/CS337-Operating-Systems/blob/925bae9d1ede96112102ce7e467705be00c7f6e8/Notes/9-%20Writing%20Xv6%20System%20Calls.pdf)
- [Project Notes](https://github.com/mattjax16/CS337-Operating-Systems/blob/925bae9d1ede96112102ce7e467705be00c7f6e8/Projects/Proj4/Project%204_%20%20Priority-based%20Scheduling%20in%20Xv6.pdf)
- [UVA XV6 Overview](https://www.cs.virginia.edu/~cr4bd/4414/S2021/xv6.html)


### Layout:
	.
    ├── Pics
    │   ├── foo_working.png
    │   └── nice_working.png
    ├── Project 4_  Priority-based Scheduling in Xv6.pdf
    ├── readme.md
    └── xv6-proj4
        ├── BUGS
        ├── LICENSE
        ├── LucidaSans-Typewriter83~
        ├── Makefile
        ├── Notes
        ├── README
        ├── TRICKS
        ├── _cat
        ├── _echo
        ├── _foo
        ├── _forktest
        ├── _grep
        ├── _init
        ├── _kill
        ├── _ln
        ├── _ls
        ├── _mkdir
        ├── _nice
        ├── _ps
        ├── _rm
        ├── _sh
        ├── _stressfs
        ├── _usertests
        ├── _wc
        ├── _zombie
        ├── asm.h
        ├── bio.c
        ├── bio.d
        ├── bio.o
        ├── bootasm.S
        ├── bootasm.d
        ├── bootasm.o
        ├── bootblock
        ├── bootblock.asm
        ├── bootblock.o
        ├── bootblockother.o
        ├── bootmain.c
        ├── bootmain.d
        ├── bootmain.o
        ├── buf.h
        ├── cat.asm
        ├── cat.c
        ├── cat.d
        ├── cat.o
        ├── cat.sym
        ├── console.c
        ├── console.d
        ├── console.o
        ├── cuth
        ├── date.h
        ├── defs.h
        ├── dot-bochsrc
        ├── echo.asm
        ├── echo.c
        ├── echo.d
        ├── echo.o
        ├── echo.sym
        ├── elf.h
        ├── entry.S
        ├── entry.o
        ├── entryother
        ├── entryother.S
        ├── entryother.asm
        ├── entryother.d
        ├── entryother.o
        ├── exec.c
        ├── exec.d
        ├── exec.o
        ├── fcntl.h
        ├── file.c
        ├── file.d
        ├── file.h
        ├── file.o
        ├── fmt
        │   ├── README
        │   ├── all.ps
        │   ├── allf.ps
        │   ├── alltext
        │   ├── asm.h
        │   ├── bio.c
        │   ├── blank
        │   ├── bootasm.S
        │   ├── bootmain.c
        │   ├── buf.h
        │   ├── console.c
        │   ├── date.h
        │   ├── defs
        │   ├── defs.h
        │   ├── elf.h
        │   ├── entry.S
        │   ├── entryother.S
        │   ├── exec.c
        │   ├── fcntl.h
        │   ├── file.c
        │   ├── file.h
        │   ├── fs.c
        │   ├── fs.h
        │   ├── ide.c
        │   ├── init.c
        │   ├── initcode.S
        │   ├── ioapic.c
        │   ├── kalloc.c
        │   ├── kbd.c
        │   ├── kbd.h
        │   ├── kernel.ld
        │   ├── lapic.c
        │   ├── log.c
        │   ├── main.c
        │   ├── memlayout.h
        │   ├── mmu.h
        │   ├── mp.c
        │   ├── mp.h
        │   ├── param.h
        │   ├── pipe.c
        │   ├── proc.c
        │   ├── proc.h
        │   ├── refs
        │   ├── s.defs
        │   ├── sh.c
        │   ├── sleeplock.c
        │   ├── sleeplock.h
        │   ├── spinlock.c
        │   ├── spinlock.h
        │   ├── stat.h
        │   ├── string.c
        │   ├── swtch.S
        │   ├── syscall.c
        │   ├── syscall.h
        │   ├── sysfile.c
        │   ├── sysproc.c
        │   ├── t.defs
        │   ├── toc
        │   ├── tocdata
        │   ├── trap.c
        │   ├── trapasm.S
        │   ├── traps.h
        │   ├── types.h
        │   ├── uart.c
        │   ├── usys.S
        │   ├── vectors.pl
        │   ├── vm.c
        │   └── x86.h
        ├── foo.asm
        ├── foo.c
        ├── foo.d
        ├── foo.o
        ├── foo.sym
        ├── forktest.asm
        ├── forktest.c
        ├── forktest.d
        ├── forktest.o
        ├── fs.c
        ├── fs.d
        ├── fs.h
        ├── fs.img
        ├── fs.o
        ├── gdbutil
        ├── grep.asm
        ├── grep.c
        ├── grep.d
        ├── grep.o
        ├── grep.sym
        ├── ide.c
        ├── ide.d
        ├── ide.o
        ├── init.asm
        ├── init.c
        ├── init.d
        ├── init.o
        ├── init.sym
        ├── initcode
        ├── initcode.S
        ├── initcode.asm
        ├── initcode.d
        ├── initcode.o
        ├── initcode.out
        ├── ioapic.c
        ├── ioapic.d
        ├── ioapic.o
        ├── kalloc.c
        ├── kalloc.d
        ├── kalloc.o
        ├── kbd.c
        ├── kbd.d
        ├── kbd.h
        ├── kbd.o
        ├── kernel
        ├── kernel.asm
        ├── kernel.ld
        ├── kernel.sym
        ├── kill.asm
        ├── kill.c
        ├── kill.d
        ├── kill.o
        ├── kill.sym
        ├── lapic.c
        ├── lapic.d
        ├── lapic.o
        ├── ln.asm
        ├── ln.c
        ├── ln.d
        ├── ln.o
        ├── ln.sym
        ├── log.c
        ├── log.d
        ├── log.o
        ├── ls.asm
        ├── ls.c
        ├── ls.d
        ├── ls.o
        ├── ls.sym
        ├── main.c
        ├── main.d
        ├── main.o
        ├── memide.c
        ├── memlayout.h
        ├── mkdir.asm
        ├── mkdir.c
        ├── mkdir.d
        ├── mkdir.o
        ├── mkdir.sym
        ├── mkfs
        ├── mkfs.c
        ├── mmu.h
        ├── mp.c
        ├── mp.d
        ├── mp.h
        ├── mp.o
        ├── nice.asm
        ├── nice.c
        ├── nice.d
        ├── nice.o
        ├── nice.sym
        ├── param.h
        ├── picirq.c
        ├── picirq.d
        ├── picirq.o
        ├── pipe.c
        ├── pipe.d
        ├── pipe.o
        ├── pr.pl
        ├── printf.c
        ├── printf.d
        ├── printf.o
        ├── printpcs
        ├── proc.c
        ├── proc.d
        ├── proc.h
        ├── proc.o
        ├── ps.asm
        ├── ps.c
        ├── ps.d
        ├── ps.o
        ├── ps.sym
        ├── rm.asm
        ├── rm.c
        ├── rm.d
        ├── rm.o
        ├── rm.sym
        ├── runoff
        ├── runoff.list
        ├── runoff.spec
        ├── runoff1
        ├── sh.asm
        ├── sh.c
        ├── sh.d
        ├── sh.o
        ├── sh.sym
        ├── show1
        ├── sign.pl
        ├── sleep1.p
        ├── sleeplock.c
        ├── sleeplock.d
        ├── sleeplock.h
        ├── sleeplock.o
        ├── spinlock.c
        ├── spinlock.d
        ├── spinlock.h
        ├── spinlock.o
        ├── spinp
        ├── stat.h
        ├── stressfs.asm
        ├── stressfs.c
        ├── stressfs.d
        ├── stressfs.o
        ├── stressfs.sym
        ├── string.c
        ├── string.d
        ├── string.o
        ├── swtch.S
        ├── swtch.o
        ├── syscall.c
        ├── syscall.d
        ├── syscall.h
        ├── syscall.o
        ├── sysfile.c
        ├── sysfile.d
        ├── sysfile.o
        ├── sysproc.c
        ├── sysproc.d
        ├── sysproc.o
        ├── toc.ftr
        ├── toc.hdr
        ├── trap.c
        ├── trap.d
        ├── trap.o
        ├── trapasm.S
        ├── trapasm.o
        ├── traps.h
        ├── types.h
        ├── uart.c
        ├── uart.d
        ├── uart.o
        ├── ulib.c
        ├── ulib.d
        ├── ulib.o
        ├── umalloc.c
        ├── umalloc.d
        ├── umalloc.o
        ├── user.h
        ├── usertests.asm
        ├── usertests.c
        ├── usertests.d
        ├── usertests.o
        ├── usertests.sym
        ├── usys.S
        ├── usys.o
        ├── vectors.S
        ├── vectors.o
        ├── vectors.pl
        ├── vm.c
        ├── vm.d
        ├── vm.o
        ├── wc.asm
        ├── wc.c
        ├── wc.d
        ├── wc.o
        ├── wc.sym
        ├── x86.h
        ├── xv6.img
        ├── zombie.asm
        ├── zombie.c
        ├── zombie.d
        ├── zombie.o
        └── zombie.sym
        

---

<br>
