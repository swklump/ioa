def batcheval_seg(output_type, start_year, end_year, savelocation, start_index, number, prefix, del_eval_choice,
                  eval_all_elements):
    import pyautogui as pg
    from .batcheval_helperfunctions import process_evals

    pg.sleep(5)
    pg.FAILSAFE = True

    # Find all coordinates that match png (little road logo for segments)
    locations = list(pg.locateAllOnScreen('PNG Files\\hwy_symbol.png'))
    # Save folder path
    savelocation = savelocation.replace('/', '\\')

    timegap = 1

    i = start_index - 1
    if eval_all_elements == 'Yes':
        elements_to_eval = len(locations)
    else:
        elements_to_eval = number + start_index - 1

    while i < elements_to_eval:

        # IF IHSDM scrolls up it won't be able to find all elements it originally saw,
        # So compare number of elements found in current view to original number found
        # If a fewer number is found, click the down arrow on the scroll bar until the
        # same number of elements is found
        curr_locations = list(pg.locateAllOnScreen('PNG Files\\hwy_symbol.png'))

        if len(curr_locations) < len(locations):
            while len(curr_locations) < len(locations):
                pg.click('PNG Files\\down.png')
                curr_locations = list(pg.locateAllOnScreen('PNG Files\\hwy_symbol.png'))

        # Right click element
        pg.click(curr_locations[i][0] + curr_locations[i][2] / 2, curr_locations[i][1] + curr_locations[i][3] / 2,
                 button='right')  # Click road logo on index i

        # "New Evaluation"
        pg.sleep(timegap)
        pg.hotkey('altleft', 'n')
        pg.sleep(3)

        # Start evaluation
        pg.hotkey('alt', 'n')
        pg.sleep(timegap)

        # Acknowledge button
        r = None
        while r is None:
            r = pg.locateOnScreen('PNG Files\\acknowledge_button.png')
        pg.click('PNG Files\\acknowledge_button.png')

        # Wait til evaluation is done
        r = None
        while r is None:
            r = pg.locateOnScreen('PNG Files\\use.png')

        # Add years of analysis
        pg.write(str(start_year))
        pg.press('tab')
        pg.write(str(end_year))
        pg.press('enter')
        pg.press('enter')
        pg.sleep(timegap)

        # Keep hitting next til there are none left
        r = None
        while r is None:
            pg.press('enter')
            pg.sleep(1)
            r = pg.locateOnScreen('PNG Files\\run.png')

        pg.sleep(timegap)

        # Hit run
        pg.press('enter')
        pg.sleep(timegap)

        # Process model evaluations
        process_evals(timegap, output_type, savelocation, prefix, del_eval_choice)

        pg.sleep(timegap)
        i += 1
