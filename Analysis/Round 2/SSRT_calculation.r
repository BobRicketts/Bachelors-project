library(plyr) 
library(reshape) 
library(ez) 
library(Hmisc) 
library(ggplot2)
library(doBy)
library(zoo) 

# --- STEP: open the data files ---
input <- data.frame()
input2 <- data.frame()

files <- list.files(path="/Users/lauritsdixen/Desktop/Bachelor/Experiment/data/executive", pattern="*.csv", full.names=TRUE, recursive=FALSE, )

i <- 0
for (file in files) {
  i = i + 1
  tmp <- read.csv(file, header = T)
  tmpR <- subset(tmp, (Response == "x" | Response == "z") | Stop_Signal == "True")
  #extract subject number
  
  
  tmp$subject <- tmp$Participant[1:length(tmp$subject)]
  tmpR$subject <- tmp$Participant[1:length(tmpR$subject)]
  
  #add the content to the data frame
  input <- rbind (input, tmpR)
  input2 <- rbind (input2, tmp)
  rm(tmp)
  rm(tmpR)
}

input$subject <- ifelse(is.na(input$subject), "NA_subject", input$subject)
input2$subject <- ifelse(is.na(input2$subject), "NA_subject", input2$subject)

# --- STEP: create some new variables ---
# create new variable for calculation of p(correct)
input$acc <- ifelse((input$Side == "right" & input$Response == "x" |input$Side == "left" & input$Response == "z"), 1, 0)
input$miss <- ifelse((input$Response != 'x' & input$Response != 'z'), 1, 0) 
input$presp <- ifelse((input$Response == 'x' | input$Response == 'z'), 1, 0) 
input$rt1 <- input$Reaction_Time
input$correct <- input$Correctness

input2$presp <- ifelse((input2$Response == 'x' | input2$Response == 'z'), 1, 0) 
# --- STEP:  do some basic design checks & basic performance ---
# check design


# check overall performance of all subjects on no-signal trials
tmp <- subset(input, Stop_Signal == "False")
prop.table(table(tmp$subject, tmp$acc), 1)

# check overall performance of all subjects on signal trials
tmp <- subset(input, Stop_Signal == 'True') 
prop.table(table(tmp$subject, tmp$acc), 1)

# --- STEP:  analyse no-signal data ---
# subset data
nosignal.input <- subset(input, Stop_Signal == "False")

# create molten object 

nosignal.molten <- melt(nosignal.input, id.var = c('subject', 'correct', 'presp'), measure.var = c('acc', 'miss', 'rt1'))

# calculate percent correct
# Accuracy of p(correct) = correct trials / (correct trials + incorrect trials).
# Trials without a response (or anticpatory responses) are omitted. 
acc.cast <- cast (nosignal.molten, subject ~ ., mean, subset = variable == "acc" &  presp == "1") 
names(acc.cast)[2] <- "acc"
acc.cast
summaryBy(acc ~ 1, data=as.data.frame(acc.cast),  FUN=c(mean,sd))

# calculate p(miss)
miss.cast <- cast (nosignal.molten, subject ~ ., mean, subset = variable == "miss") 
names(miss.cast)[2] <- "miss"
miss.cast
summaryBy(miss ~ 1, data=as.data.frame(miss.cast),  FUN=c(mean,sd))

# calculate RT for correct responses
rt.cast <- cast (nosignal.molten,  subject ~ ., mean, subset = variable == "rt1" &  correct == "True") 
names(rt.cast)[2] <- "rt"
rt.cast
summaryBy(rt ~ 1, data=as.data.frame(rt.cast),  FUN=c(mean,sd))

# --- STEP:  analyse stop-signal data ---

#function to calculate all signal data at once...
funcSignal <- function(data){
  # signal data: prespond & ssd
  signal <- subset(data, Stop_Signal == 'True')
  presp <-  mean(signal$presp)
  ssd <- mean(signal$SSD)
  
  # nth RT & mean go RT
  nosignal <- subset(data, Stop_Signal == 'False')
  nthRT <- quantile(nosignal$Reaction_Time[1:length(nosignal$Reaction_Time)],probs = presp, type = 6)
  goRT <- mean(nosignal$Reaction_Time)
  
  # SSRT = nthRT - ssd
  ssrt <- nthRT - ssd
  
  # signal-respond RT
  responded <- subset(signal, presp == 1)
  sRT <- mean(responded$Reaction_Time)
  raceTest <- goRT - sRT
  
  # Return
  return(data.frame(subject = data$subject[1], presp = presp, ssd = ssd, nthRT = nthRT, ssrt = ssrt, 
                    sRT = sRT, raceTest = raceTest))
}

data <- tmp
input2$subject <- as.factor(input2$subject)
signal.cast <- data.frame()
for (s in levels(input2$subject)) {
  tmp <- subset(input2, subject == s)
  vals <- funcSignal(tmp)
  signal.cast <- rbind(signal.cast, vals)
}



# combine all data and write to csv file
combined <- signal.cast
combined$acc.ns <- acc.cast$acc
combined$rt.ns <- rt.cast$rt
write.csv(combined, 'combined.csv')