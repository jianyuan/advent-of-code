package main

import (
	"flag"
	"io/ioutil"
	"log"
	"math"
	"strconv"
	"strings"
	"sync"

	"github.com/gitchander/permutation"
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

type InputReader interface {
	Read() int
}

type OutputWriter interface {
	Write(int)
}

type CPU struct {
	id     int
	pc     int
	Memory []int

	InputReader  InputReader
	OutputWriter OutputWriter
}

func (cpu *CPU) getValue(offset int, write bool) int {
	positionCodes := cpu.Memory[cpu.pc] / 100
	instructionMode := instructionModes[getDigit(positionCodes, offset)]
	return instructionMode(cpu, cpu.Memory[cpu.pc+1+offset], write)
}

func (cpu *CPU) RunUntilFinish() {
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
			value := cpu.InputReader.Read()
			// log.Println(cpu.id, "Input:", value)
			cpu.Memory[w] = value
			cpu.pc += 2
		case 4: // print
			a := cpu.getValue(0, false)
			// log.Println(cpu.id, "Output:", a)
			cpu.OutputWriter.Write(a)
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

func runCPU(id int, memory []int, inputReader InputReader, outputWriter OutputWriter) *CPU {
	cpu := &CPU{
		id:           id,
		Memory:       append([]int{}, memory...),
		InputReader:  inputReader,
		OutputWriter: outputWriter,
	}
	cpu.RunUntilFinish()
	return cpu
}

type SliceInputReader struct {
	Data    []int
	pointer int
}

func (s *SliceInputReader) Read() int {
	value := s.Data[s.pointer]
	s.pointer++
	return value
}

type SliceOutputWriter struct {
	Data []int
}

func (s *SliceOutputWriter) Write(value int) {
	s.Data = append(s.Data, value)
}

type ChanInputReader struct {
	done chan bool
	Ch   chan int
}

func (c *ChanInputReader) Read() int {
	return <-c.Ch
}

type ChanOutputWriter struct {
	Ch chan int
}

func (c *ChanOutputWriter) Write(value int) {
	c.Ch <- value
}

var inputFilename string

func init() {
	flag.StringVar(&inputFilename, "input", "input.txt", "Input file name")
}

func part1(memory []int) int {
	var maxResult int

	phaseSettings := []int{0, 1, 2, 3, 4}
	p := permutation.New(permutation.IntSlice(phaseSettings))
	for p.Next() {
		var lastOutput int
		for _, phaseSetting := range phaseSettings {
			reader := &SliceInputReader{Data: []int{phaseSetting, lastOutput}}
			writer := &SliceOutputWriter{}
			runCPU(0, memory, reader, writer)
			lastOutput = writer.Data[0]
		}
		if lastOutput > maxResult {
			maxResult = lastOutput
		}
	}

	return maxResult
}

func part2(memory []int) int {
	var maxResult int

	phaseSettings := []int{5, 6, 7, 8, 9}
	p := permutation.New(permutation.IntSlice(phaseSettings))
	for p.Next() {

		// fmt.Println("==> Trying", phaseSettings)

		var firstReader *ChanInputReader
		var lastWriter *ChanOutputWriter
		var wg sync.WaitGroup

		for id, phaseSetting := range phaseSettings {
			reader := &ChanInputReader{Ch: make(chan int, 1)}
			writer := &ChanOutputWriter{Ch: make(chan int, 1)}

			// fmt.Println("==> Launching", id, phaseSetting, reader, writer)

			wg.Add(1)
			go func(wg *sync.WaitGroup, id int, reader *ChanInputReader, writer *ChanOutputWriter) {
				defer wg.Done()
				runCPU(id, memory, reader, writer)
			}(&wg, id, reader, writer)

			if lastWriter != nil {
				go func(lastWriter *ChanOutputWriter, reader *ChanInputReader) {
					for {
						select {
						case value := <-lastWriter.Ch:
							reader.Ch <- value
						}
					}
				}(lastWriter, reader)
			}

			lastWriter = writer

			reader.Ch <- phaseSetting

			if firstReader == nil {
				reader.Ch <- 0
				firstReader = reader
			}
		}

		// feedback loop
		go func(lastWriter *ChanOutputWriter, firstReader *ChanInputReader) {
			for {
				select {
				case value := <-lastWriter.Ch:
					firstReader.Ch <- value
				}
			}
		}(lastWriter, firstReader)

		wg.Wait()

		lastOutput := <-firstReader.Ch

		if lastOutput > maxResult {
			maxResult = lastOutput
		}
	}

	return maxResult
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

	log.Println("Part 1:", part1(memory))
	log.Println("Part 2:", part2(memory))
}
