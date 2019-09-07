/*
 * log.c - A logging facility for debugging
 *
 * Copyright (C) 1995-1998 David Firth
 * Copyright (C) 1998-2005 Atari800 development team (see DOC/CREDITS)
 *
 * This file is part of the Atari800 emulator project which emulates
 * the Atari 400, 800, 800XL, 130XE, and 5200 8-bit computers.
 *
 * Atari800 is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Atari800 is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Atari800; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/

#define _POSIX_C_SOURCE 200112L /* for vsnprintf */

#include "config.h"
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdbool.h>
#ifdef ANDROID
#include <android/log.h>
#endif

#include "log.h"

char *LOG_FILE_PATH;
bool LOG_DEBUG_SDL_BUTTONS = 0;
FILE *LOG_FP = 0;

int Log_ReadConfig(char string[], char *ptr) {
	if (strcmp(string, "LOG_DEBUG_SDL_BUTTONS") == 0) {
		if (strcmp("1", ptr) == 0) {
			LOG_DEBUG_SDL_BUTTONS = 1;
			return 1;
		}
	}
	if (strcmp(string, "LOGFILE") == 0) {
		LOG_FILE_PATH = strdup(ptr);
		Log_println("Opening logfile %s.\n", LOG_FILE_PATH);
 		LOG_FP = fopen(LOG_FILE_PATH, "w");
		Log_println("Logfile %s opened for writing.\n", LOG_FILE_PATH);
		return 1;
	}
	return 0;
}

void Log_WriteConfig(FILE *fp) {
	fprintf(fp, "LOGFILE=%s\n", LOG_FILE_PATH);
	fprintf(fp, "LOG_DEBUG_SDL_BUTTONS=%d\n", LOG_DEBUG_SDL_BUTTONS);
}

void Log_print(char *format, ...) {
	va_list args;
	va_start(args, format);
	if (LOG_FP) {
		vfprintf(LOG_FP, format, args);
	} else {
		vfprintf(stdout, format, args);
	}
	Log_flushlog();
	va_end(args);
}

void Log_println(char *format, ...) {
	va_list args;
	va_start(args, format);
	if (LOG_FP) {
		vfprintf(LOG_FP, format, args);
		fprintf(LOG_FP, "\n");
	} else {
		vfprintf(stdout, format, args);
		fprintf(stdout, "\n");
	}
	Log_flushlog();
	va_end(args);
}

void Log_flushlog(void)
{
	if (LOG_FP) {
		fflush(LOG_FP);
	}
}
