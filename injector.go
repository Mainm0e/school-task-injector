package main

import (
	"io/ioutil"
	"log"
	"os"
)

func mergePrograms(targetBinaryPath, injectorBinaryPath string) error {
	// Read the injector binary
	injectorBinary, err := ioutil.ReadFile(injectorBinaryPath)
	if err != nil {
		return err
	}

	// Open the target binary in append mode
	targetFile, err := os.OpenFile(targetBinaryPath, os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	defer targetFile.Close()

	// Write the injector binary to the end of the target binary
	_, err = targetFile.Write(injectorBinary)
	if err != nil {
		return err
	}

	log.Printf("Injected %s into %s\n", injectorBinaryPath, targetBinaryPath)
	return nil
}

func main() {
	if len(os.Args) != 3 {
		log.Fatalf("Usage: %s <target> <injector>", os.Args[0])
	}

	target := os.Args[1]
	injector := os.Args[2]

	err := mergePrograms(target, injector)
	if err != nil {
		log.Fatal(err)
	}
}
