import React, { useState } from 'react'
import { enGB } from 'date-fns/locale'
import { DatePicker } from 'react-nice-dates'
import 'react-nice-dates/build/style.css'
function DateInput() {
  const [date, setDate] = useState(new Date(2020, 1, 24, 18, 15))
  return (
    <DatePicker date={date} onDateChange={setDate} locale={enGB} format='dd-MM-yyyy'>
      {({ inputProps, focused }) => <input className={'input' + (focused ? ' -focused' : '')} {...inputProps} />}
    </DatePicker>
  )
}

export default DateInput;