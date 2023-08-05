Select EventLog,RecordNumber,TO_UTCTIME(TimeGenerated) as TimeGeneratedUTC,TO_UTCTIME(TimeWritten) as TimeWrittenUTC,EventID,EventType,EventTypeName,EventCategory,EventCategoryName,SourceName,REPLACE_CHR(Strings, '\u000a\u000d,', ' ') as Strings,ComputerName,SID,RESOLVE_SID(SID) as ResolvedSID,REPLACE_CHR(Message, '\u000a\u000d,', ' ') as Message,REPLACE_CHR(Data, '\u000a\u000d,', ' ') as Data from Security
