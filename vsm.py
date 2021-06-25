class VSM:
  def __init__(self):
    self.internal_bus = 0b0000

    self.progmem = self.ProgMem()
    self.progmem.import_data("rom.txt")

    self.micro_instr = self.MicroInstructions(self)
    self.registers = self.Registers(self)
    self.alu = self.ALU(self)

  def clock_cycle(self):
    # Counter
    for clk in self.progmem.mem_content:
      self.registers.main_reg = clk
      self.write_bus(self.registers.main_reg[4:])
      self.registers.accb = self.internal_bus
      self.micro_instr.exec_instr(self.registers.main_reg)

  def write_bus(self, data):
    self.internal_bus = data


  class MicroInstructions:
    def __init__(self, VSM):
      self.instructions = {
        "0000": self.NOP,
        "0001": self.ADD,
        "0010": self.SUB,
        "0011": self.IN,
        "0100": self.OUT,
        "0101": self.LDA
      }

      self.VSM = VSM

    def exec_instr(self, instr):
      self.instructions[instr[:4]](int(instr[4:], 2))

    def NOP(self, data):
      pass

    def ADD(self, data):
      self.VSM.registers.accb = data
      self.VSM.alu.enable_alu(1)

    def SUB(self, data):
      self.VSM.registers.accb = data
      self.VSM.alu.enable_alu(0)

    def IN(self, data):
      self.VSM.registers.acca = int(input(), 2)

    def OUT(self, data):
      self.VSM.internal_bus = str(bin(self.VSM.registers.acca))
      print(self.VSM.internal_bus)

    def LDA(self, data):
      self.VSM.registers.acca = data


  class ProgMem:
    def __init__(self):
      self.mem_content = []

    def import_data(self, filename):
      with open(filename, "r") as data:
        for line in data:
          self.mem_content.append(line.strip())


  class Registers:
    def __init__(self, VSM):
      self.VSM = VSM
      self.acca      = 0b0000
      self.accb      = 0b0000
      self.main_reg  = "00000000"

    def enable_a(self):
      self.VSM.write_bus(self.acca)

    def load_b(self):
      self.accb = self.VSM.internal_bus

    def load_a(self):
      self.acca = self.VSM.internal_bus

    def enable_instr(self):
      self.VSM.write_bus(main_reg[:4])


  class ALU:
    def __init__(self, VSM):
      self.VSM = VSM

    def enable_alu(self, mode):
      (self.add if mode else self.sub)()

    def add(self):
      self.VSM.registers.acca += self.VSM.registers.accb

    def sub(self):
      self.VSM.registers.acca -= self.VSM.registers.accb


VSM().clock_cycle()
