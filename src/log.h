#ifndef LOG_H_
#define LOG_H_

int Log_ReadConfig(char string[], char *ptr);
void Log_WriteConfig(FILE *fp);
void Log_print(char *format, ...);
void Log_println(char *format, ...);
void Log_flushlog(void);

#endif /* LOG_H_ */
