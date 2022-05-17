def batcheval_int(output_type, start_year, end_year, savelocation, start_index, number, prefix, del_eval_choice,
                  eval_all_elements):
    import pyautogui as pg
    from .batcheval_helperfunctions import process_evals

    pg.sleep(5)
    pg.FAILSAFE = True

    locations = list(pg.locateAllOnScreen('PNG Files\\int_symbol.png'))
    # Save folder path
    savelocation = savelocation.replace('/', '\\')

    timegap = 0.5

    i = start_index - 1
    if eval_all_elements == 'Yes':
        elements_to_eval = len(locations)
    else:
        elements_to_eval = number + start_index - 1

    while i < elements_to_eval:

        curr_locations = list(pg.locateAllOnScreen('PNG Files\\int_symbol.png'))

        if len(curr_locations) < len(locations):
            while len(curr_locations) < len(locations):
                pg.click('PNG Files\\down.png')
                curr_locations = list(pg.locateAllOnScreen('PNG Files\\int_symbol.png'))

        # Right-click the interchange symbol to pull up the contextual menu
        pg.click(curr_locations[i][0] + curr_locations[i][2] / 2, curr_locations[i][1] + curr_locations[i][3] / 2,
                 button='right')
        pg.sleep(timegap)
        pg.hotkey('alt', 'n')

        # Go through first window, evaluation settings
        r = None
        while r is None:
            r = pg.locateOnScreen('PNG Files\\first_year.png')
        pg.click('PNG Files\\first_year.png')

        rampterminals = list(pg.locateAllOnScreen('PNG Files\\rampterminal.png'))

        pg.write(str(start_year))
        pg.press('tab')
        pg.write(str(end_year))
        pg.press('enter')
        pg.press('enter')

        # Go through 2nd window, no action needed
        pg.sleep(timegap)
        pg.press('enter')
        pg.sleep(timegap)

        # Go through 3rd window, run evals
        evals = list(pg.locateAllOnScreen('PNG Files\\box.png'))

        # Looping through the ramp segments
        for j in range(len(evals) - len(rampterminals)):

            # Click the box and run eval
            pg.click(evals[j][0] + evals[j][2] / 2, evals[j][1] + evals[j][3] / 2)
            pg.sleep(timegap)
            pg.hotkey('alt', 'a')

            # Start new window
            pg.sleep(3)
            pg.hotkey('alt', 'n')
            pg.sleep(timegap)

            # Acknowledge button
            r = None
            while r is None:
                r = pg.locateOnScreen('PNG Files\\acknowledge_button.png')
            pg.click('PNG Files\\acknowledge_button.png')

            # Wait til evaluation done
            r = None
            while r is None:
                r = pg.locateOnScreen('PNG Files\\use.png')
            pg.sleep(timegap)

            # first window
            pg.press('enter')
            pg.press('enter')
            pg.sleep(timegap)
            # second window
            pg.press('enter')
            pg.sleep(timegap)
            # third window
            pg.press('enter')
            pg.sleep(timegap)
            # Press run window
            pg.press('enter')
            pg.sleep(timegap)

            # Process evaluations
            process_evals(timegap, output_type, savelocation, prefix, del_eval_choice)

        # Looping through the ramp terminals
        for k in range(len(rampterminals)):

            # Click white box
            pg.click(
                evals[k + (len(evals) - len(rampterminals))][0] + evals[k + (len(evals) - len(rampterminals))][2] / 2,
                evals[k + (len(evals) - len(rampterminals))][1] + evals[k + (len(evals) - len(rampterminals))][3] / 2)
            pg.sleep(timegap)

            # Run eval
            pg.hotkey('altleft', 'a')
            pg.sleep(3)

            # Press acknowledge
            r = None
            while r is None:
                r = pg.locateOnScreen('PNG Files\\acknowledge_button.png')
            pg.click('PNG Files\\acknowledge_button.png')
            pg.sleep(timegap)

            # 2nd window
            pg.press('enter')
            pg.sleep(timegap)

            # Press run
            pg.press('enter')
            pg.sleep(timegap)

            # Process evaluations
            process_evals(timegap, output_type, savelocation, prefix, del_eval_choice)

        pg.click('PNG Files\\return.png')
        pg.hotkey('alt', 'c')
        r = None
        while r is None:
            r = pg.locateOnScreen('PNG Files\\collapse.png')
        pg.click('PNG Files\\collapse.png')
        pg.sleep(timegap)
        pg.scroll(1000)
        i += 1
