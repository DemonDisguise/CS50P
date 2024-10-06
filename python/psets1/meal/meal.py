def main():
    time = input("What time is it? ").strip()
    timer = convert(time)
    timer_format = (time.endswith("a.m.") or time.endswith("p.m."))

    match timer_format:
        case False:
            if 7.0 <= timer <= 8.0:
                print("breakfast time")
            elif 12.0 <= timer <= 13.0:
                print("lunch time")
            elif 18.0 <= timer <= 19.0:
                print("dinner time")
        case True:
            if time.endswith("a.m."):
                if 7.0 <= timer <= 8.0:
                    print("breakfast time")
            elif time.endswith("p.m."):
                if 12.0 <= timer < 13.0 or timer == 1.0:
                    print("lunch time")
                elif 6.0 <= timer <= 7.0:
                    print("dinner time")


def convert(time):
     time_format = (time.endswith("a.m.") or time.endswith("p.m."))
     match time_format:
         case False:
             hours, minutes = time.split(":")
             minutes = int(minutes) / 60
             return float(int(hours) + minutes)
         case True:
             timer, meridian = time.split()
             hours, minutes = timer.split(":")
             minutes = int(minutes) / 60
             return float(int(hours) + minutes)


if __name__ == "__main__":
    main()

