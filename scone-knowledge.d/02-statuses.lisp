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

;; ---------- inhabited/uninhabited place
(new-type {inhabited place} {place})
(new-type {uninhabited place} {place})
(new-complete-split {place}
 '({inhabited place}
   {uninhabited place}))

(new-indv {inhabited} {status})
(new-indv {uninhabited} {status})

(new-type-role {place status} {place} {status})
(x-is-the-y-of-z {inhabited} {place status} {inhabited place})
(x-is-the-y-of-z {uninhabited} {place status} {uninhabited place})

;; ########## SPECIFIC STATUSES ##########
;; ---------- Illumination
(new-indv {on light source} {light source})
(new-is-a {on light source} {on device})
(new-indv {off light source} {light source})
(new-is-a {off light source} {off device})

;; ---------- Occupation
(new-indv {inhabited room} {inhabited place})
(new-indv {uninhabited room} {uninhabited place})
