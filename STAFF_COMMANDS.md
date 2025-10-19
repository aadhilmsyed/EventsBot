# 🛡️ GeoFS Events CoPilot - Staff Commands

> **For First Officers and Captains**

This document contains all administrative commands for the GeoFS Events CoPilot bot. These commands are restricted to staff members only.

---

## 📋 **Command Categories**

- 🛡️ **First Officer Commands** - Channel, member, flight time, and event management
- 👑 **Captain Commands** - Event control, role management, and system management
- ⚠️ **Important Notes** - Safety warnings and troubleshooting

---

## 🛡️ **First Officer Commands**

*Available to: First Officers, Captains*

### 📺 **Channel Management**

**`!restrict`**
- **Description:** Add channels to restricted list
- **Usage:** `!restrict #channel1 #channel2`
- **Example:** `!restrict #general #announcements`

**`!unrestrict`**
- **Description:** Remove channels from restricted list
- **Usage:** `!unrestrict #channel1 #channel2`
- **Example:** `!unrestrict #general`

**`!view_restricted_channels`**
- **Description:** List all restricted channels
- **Usage:** `!view_restricted_channels`

**`!add_event_vc`**
- **Description:** Add voice channels for event logging
- **Usage:** `!add_event_vc #voice1 #voice2`
- **Example:** `!add_event_vc #event-voice #main-voice`

**`!remove_event_vc`**
- **Description:** Remove voice channels from event logging
- **Usage:** `!remove_event_vc #voice1 #voice2`
- **Example:** `!remove_event_vc #old-event-voice`

**`!view_event_vc`**
- **Description:** List all event voice channels
- **Usage:** `!view_event_vc`

### 👥 **Member Management**

**`!blacklist`**
- **Description:** Add member to command blacklist
- **Usage:** `!blacklist @member`
- **Example:** `!blacklist @spammer`

**`!whitelist`**
- **Description:** Remove member from blacklist
- **Usage:** `!whitelist @member`
- **Example:** `!whitelist @reformed-user`

**`!view_blacklist`**
- **Description:** List all blacklisted members
- **Usage:** `!view_blacklist`

### ⏱️ **Flight Time Management**

**`!add_flight_time`**
- **Description:** Add flight time to member
- **Usage:** `!add_flight_time @member <minutes>`
- **Example:** `!add_flight_time @pilot 120` (adds 2 hours)

**`!remove_flight_time`**
- **Description:** Remove flight time from member
- **Usage:** `!remove_flight_time @member <minutes>`
- **Example:** `!remove_flight_time @pilot 60` (removes 1 hour)

**`!view_flight_time`**
- **Description:** Export comprehensive flight data
- **Usage:** `!view_flight_time`
- **Note:** Sends detailed flight data file to log channel

### 📅 **Event Management**

**`!add_event_attendance`**
- **Description:** Add member to event attendance
- **Usage:** `!add_event_attendance @member "Event Name"`
- **Example:** `!add_event_attendance @pilot "Monthly Flight Event"`

**`!remove_event_attendance`**
- **Description:** Remove member from event attendance
- **Usage:** `!remove_event_attendance @member "Event Name"`
- **Example:** `!remove_event_attendance @pilot "Monthly Flight Event"`

**`!view_event_attendance`**
- **Description:** View attendance for specific event
- **Usage:** `!view_event_attendance "Event Name"`
- **Example:** `!view_event_attendance "Monthly Flight Event"`

---

## 👑 **Captain Commands**

*Available to: Captains Only*

### 🎯 **Event Control**

**`!start_event`**
- **Description:** Start unofficial event logging
- **Usage:** `!start_event "Event Name"`
- **Example:** `!start_event "Emergency Flight Session"`
- **Note:** Automatically starts flight hour logging

**`!end_event`**
- **Description:** End current event
- **Usage:** `!end_event`
- **Note:** Stops flight hour logging and saves data

**`!add_event`**
- **Description:** Add event to database
- **Usage:** `!add_event "Event Name"`
- **Example:** `!add_event "Weekly Training Flight"`

**`!remove_event`**
- **Description:** Remove event from database
- **Usage:** `!remove_event "Event Name"`
- **Example:** `!remove_event "Cancelled Event"`

### 🎖️ **Role Management**

**`!update_roles`**
- **Description:** Update all member roles based on flight hours
- **Usage:** `!update_roles`
- **⚠️ Warning:** This process may take several minutes
- **Note:** Removes all rank roles first, then adds earned roles

**`!clear_flight_logs`**
- **Description:** Clear all flight hour data
- **Usage:** `!clear_flight_logs`
- **⚠️ Warning:** This permanently deletes all flight data
- **Note:** Use with extreme caution

### ⚙️ **System Management**

**`!view_flight_time`**
- **Description:** Export comprehensive flight data
- **Usage:** `!view_flight_time`
- **Note:** Same as First Officer command, sends detailed data file

**`!view_event_vc`**
- **Description:** Manage event voice channels
- **Usage:** `!view_event_vc`
- **Note:** Same as First Officer command

**`!view_restricted_channels`**
- **Description:** Manage restricted channels
- **Usage:** `!view_restricted_channels`
- **Note:** Same as First Officer command

---

## ⚠️ **Important Notes**

### **Role Update Process**
- `!update_roles` processes all members and may take several minutes
- The command removes all rank roles first, then adds earned roles
- Progress is logged to the log channel
- **Do not run multiple role updates simultaneously**

### **Data Management**
- `!clear_flight_logs` **permanently deletes** all flight data
- All changes are automatically logged to the log channel
- Flight hours are automatically saved after each operation

### **Event System**
- Event commands automatically start/stop flight hour logging
- Voice channel monitoring is automatic during events
- Members are automatically logged when joining/leaving event voice channels

### **Permission Levels**
- **First Officer**: Channel management, member management, flight time management, event management
- **Captain**: All First Officer commands + event control + role management + system management

### **Safety Features**
- All commands have built-in error handling
- Invalid inputs are rejected with clear error messages
- Bot filtering prevents bots from being logged
- Rate limiting prevents Discord API issues

---

## 🔧 **Troubleshooting**

### **Common Issues**
1. **Command not working**: Check bot permissions and your role
2. **Role updates failing**: Ensure bot's role is higher than target roles
3. **Flight logging issues**: Verify voice channel permissions
4. **Data not saving**: Check bot's file write permissions

### **Getting Help**
- Check the log channel for error messages
- Verify bot permissions in Discord server settings
- Ensure all required environment variables are set
- Contact bot developer for technical issues

---

*Last Updated: Version 2.3*
*Developed by GeoFS Flights Channel*
