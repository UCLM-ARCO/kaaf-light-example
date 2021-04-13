(in-context {general})

;; Two types of event?:
;; - Event provides data: "temperature: 24ºC"
;; - Event is the data itself: "motion"

;; {event} defined in the core
(new-type {event with data} {event})
(new-type {dataless event} {event})

;; ---------- Dataless events
(new-indv {motion event} {dataless event})

;; ---------- Events with data
(new-indv {temperature event} {event with data})


