package main

import (
	"bufio"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

type InstructionMode func(cpu *CPU, value int, write bool) int

func PositionMode(cpu *CPU, value int, write bool) int {
	if write {
		return value
	}
	return cpu.Memory[value]
}

func ImmediateMode(cpu *CPU, value int, write bool) int {
	return value
}

var (
	instructionModes = map[int]InstructionMode{
		0: PositionMode,
		1: ImmediateMode,
	}
)

func getDigit(n, digit int) int {
	return (n / int(math.Pow10(digit))) % 10
}

type CPU struct {
	pc     int
	Memory []int
}

func (cpu *CPU) getValue(offset int, write bool) int {
	positionCodes := cpu.Memory[cpu.pc] / 100
	instructionMode := instructionModes[getDigit(positionCodes, offset)]
	return instructionMode(cpu, cpu.Memory[cpu.pc+1+offset], write)
}

func (cpu *CPU) RunUntilFinish() {
	var err error

	scanner := bufio.NewScanner(os.Stdin)

	for cpu.pc < len(cpu.Memory) {
		fullOpcode := cpu.Memory[cpu.pc]
		opcode := fullOpcode % 100

		// fmt.Println("==> opcode", fullOpcode)
		// fmt.Println("==> pc before", cpu.pc)
		// fmt.Println("==> before", cpu.Memory)

		switch opcode {
		case 1: // add
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			w := cpu.getValue(2, true)
			cpu.Memory[w] = a + b
			cpu.pc += 4
		case 2: // multiply
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			w := cpu.getValue(2, true)
			cpu.Memory[w] = a * b
			cpu.pc += 4
		case 3: // store
			w := cpu.getValue(0, true)
			fmt.Println("Input:")

			var rawInt int64

			for {
				scanner.Scan()
				rawInt, err = strconv.ParseInt(scanner.Text(), 10, 64)
				if err == nil {
					break
				}
				log.Fatal(err)
			}

			cpu.Memory[w] = int(rawInt)
			cpu.pc += 2
		case 4: // print
			a := cpu.getValue(0, false)
			log.Println("Output:", a)
			cpu.pc += 2
		case 5: // jump-if-true
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			if a != 0 {
				cpu.pc = b
			} else {
				cpu.pc += 3
			}
		case 6: // jump-if-false
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			if a == 0 {
				cpu.pc = b
			} else {
				cpu.pc += 3
			}
		case 7: // less than
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			w := cpu.getValue(2, true)

			if a < b {
				cpu.Memory[w] = 1
			} else {
				cpu.Memory[w] = 0
			}
			cpu.pc += 4
		case 8: // equals
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			w := cpu.getValue(2, true)

			if a == b {
				cpu.Memory[w] = 1
			} else {
				cpu.Memory[w] = 0
			}
			cpu.pc += 4
		case 99: // stop
			return
		default:
			log.Fatalln("Opcode not implemented:", opcode, "PC:", cpu.pc)
		}

		// fmt.Println("<== pc after", cpu.pc)
		// fmt.Println("<== after", cpu.Memory)
	}
}

func runCPU(input []int) {
	memory := make([]int, len(input))
	copy(memory, input)
	cpu := &CPU{
		Memory: memory,
	}
	cpu.RunUntilFinish()
}

var inputFilename string

func init() {
	flag.StringVar(&inputFilename, "input", "input.txt", "Input file name")
}

func main() {
	var err error

	flag.Parse()

	inputData, err := ioutil.ReadFile(inputFilename)
	if err != nil {
		log.Fatal(err)
	}

	rawInput := strings.TrimSpace(string(inputData))
	rawInputNumbers := strings.Split(rawInput, ",")

	memory := make([]int, 0, len(rawInputNumbers))
	for _, rawInputNumber := range rawInputNumbers {
		rawInt, err := strconv.ParseInt(rawInputNumber, 10, 64)
		if err != nil {
			log.Fatal(err)
		}
		memory = append(memory, int(rawInt))
	}

	runCPU(input)
}
