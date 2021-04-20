(in-context {general})

;; ########## STATUSES / QUALITIES ##########
(new-type {quality} {thing})
(new-type {status} {quality})

;; ---------- on/off device
(new-type {on device} {device})
(new-type {off device} {device})
(new-complete-split {device}
 '({on device}
   {off device}))

(new-indv {on} {status})
(new-indv {off} {status})

(new-type-role {device status} {device} {status})
(x-is-the-y-of-z {on} {device status} {on device})
(x-is-the-y-of-z {off} {device status} {off device})

;; ---------- occupied/unoccupied place
(new-type {occupied place} {place})
(new-type {unoccupied place} {place})
(new-complete-split {place}
 '({occupied place}
   {unoccupied place}))

(new-indv {occupied} {status})
(new-indv {unoccupied} {status})

(new-type-role {occupation status} {place} {status})
(x-is-the-y-of-z {occupied} {occupation status} {occupied place})
(x-is-the-y-of-z {unoccupied} {occupation status} {unoccupied place})

;; ########## SPECIFIC STATUSES ##########
;; ---------- Illumination
(new-indv {on light source} {light source})
(new-is-a {on light source} {on device})
(new-indv {off light source} {light source})
(new-is-a {off light source} {off device})

;; ---------- Occupation
(new-indv {occupied room} {occupied place})
(new-indv {unoccupied room} {unoccupied place})
