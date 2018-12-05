# MixGuess

### Hassan Harb
### December 4, 2018

MixGuess reads in two fchk files and saves their Alpha and Beta MO Coefficient matrices.
The script then creates a new checkpoint file that has a new set of MOs where the alpha and beta MOs are copied from the two chkpt files respectively

   usage: python MixGuess.py Job1.fchk Job2.fchk flag

   flag indiacates the choice of MOs, 4 options are available:

        aa: Alpha MOs from chkpt1 -> Alpha MOs to chkpt 3
            Alpha MOs from chkpt2 -> Beta MOs to chkpt 3

        ab: Alpha MOs from chkpt1 -> Alpha MOs to chkpt 3
            Beta MOs from chkpt2 -> Beta MOs to chkpt 3

        ba: Beta MOs from chkpt1 -> Alpha MOs to chkpt 3
            Alpha MOs from chkpt2 -> Beta MOs to chkpt 3

        bb: Beta MOs from chkpt1 -> Alpha MOs to chkpt 3
            Beta MOs from chkpt2 -> Beta MOs to chkpt 3
            
            
