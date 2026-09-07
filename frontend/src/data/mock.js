// Mock data for Bengali Association Coimbatore - Enhanced Version

export const heroSlides = [
  {
    id: 1,
    image: 'https://images.unsplash.com/photo-1616074385287-67f6fb9e9eb8?w=1920&q=80',
    kicker: 'Est. 2002 · Regd. No. 189/2002',
    title: 'The Bengali Association',
    accent: 'Coimbatore',
    subtitle: 'A close-knit community celebrating Bengali culture, traditions, heritage and the values of Bengal in the heart of the south.',
    cta: { label: 'Explore Durga Puja 2026', href: '#events' },
  },
  {
    id: 2,
    image: 'https://images.unsplash.com/photo-1617875216004-78f15839c578?w=1920&q=80',
    kicker: 'Our Spirit',
    title: 'Keeping the Spirit of',
    accent: 'Bengal Alive',
    subtitle: 'From Durga Puja to Saraswati Puja, from Rabindra Sangeet to community service — we live Bengal, everyday.',
    cta: { label: 'View Puja Schedule', href: '#events' },
  },
  {
    id: 3,
    image: 'https://images.unsplash.com/photo-1645264090488-a019de493023?w=1920&q=80',
    kicker: 'Our Pride',
    title: 'বাংলার মাটি,',
    accent: 'বাংলার সংস্কৃতি',
    subtitle: 'আমাদের গরবা — the soil of Bengal, the culture of Bengal, our pride. Carried forward with love in Coimbatore.',
    cta: { label: 'Discover Our Heritage', href: '#pillars' },
  },
  {
    id: 4,
    image: '/community-group.webp',
    kicker: 'Join The Family',
    title: 'Become a',
    accent: 'Member',
    subtitle: 'Be part of a vibrant community that celebrates festivals, fosters friendship, and preserves the timeless traditions of Bengal.',
    cta: { label: 'Become a Member', href: '#membership' },
  },
];

export const stats = [
  { value: '25', suffix: 'th', label: 'Year of Durga Puja' },
  { value: '500', suffix: '+', label: 'Active Members' },
  { value: '2002', suffix: '', label: 'Established' },
  { value: '15', suffix: '+', label: 'Annual Events' },
];

// Durga Puja 2026 schedule with detailed timings
export const events = [
  {
    id: 1,
    date: 'Oct 16',
    day: 'Friday',
    title: 'Maha Shashti',
    sessions: [
      { time: '9:28 AM – 3:43 PM', name: 'Shashti Puja', note: 'Bodhon of Devi Durga' },
      { time: '7:00 PM', name: 'Cultural Function', note: 'Opening evening' },
    ],
    accent: 'saffron',
  },
  {
    id: 2,
    date: 'Oct 17',
    day: 'Saturday',
    title: 'Maha Saptami · Day 1',
    sessions: [
      { time: '9:29 AM', name: 'Saptami Puja', note: 'Kola Bou snan & sthapan' },
      { time: '12:00 PM', name: 'Pushpanjali', note: 'Floral offering' },
      { time: '12:30 PM', name: 'Bhog Arati', note: 'Community bhog' },
      { time: '8:00 PM', name: 'Sandhya Arati', note: 'Evening arati & cultural night' },
    ],
    accent: 'crimson',
  },
  {
    id: 3,
    date: 'Oct 18',
    day: 'Sunday',
    title: 'Maha Saptami · Day 2',
    sessions: [
      { time: '12:00 PM', name: 'Pushpanjali', note: 'Floral offering' },
      { time: '12:30 PM', name: 'Bhog Arati', note: 'Community bhog' },
      { time: '8:00 PM', name: 'Sandhya Arati', note: 'Cultural function' },
    ],
    accent: 'gold',
  },
  {
    id: 4,
    date: 'Oct 19',
    day: 'Monday',
    title: 'Maha Ashtami',
    sessions: [
      { time: '5:43 AM – 10:00 AM', name: 'Ashtami Puja', note: 'Main morning puja' },
      { time: '7:26 AM', name: 'Sandhi Puja', note: 'The most sacred moment' },
      { time: '8:14 AM', name: 'Bhog Arati', note: 'Morning bhog' },
      { time: '8:00 PM', name: 'Sandhya Arati', note: 'Cultural evening' },
    ],
    accent: 'terracotta',
  },
  {
    id: 5,
    date: 'Oct 20',
    day: 'Tuesday',
    title: 'Maha Nabami',
    sessions: [
      { time: '5:40 AM – 9:31 AM', name: 'Nabami Puja', note: 'Morning rituals' },
      { time: '10:00 AM', name: 'Pushpanjali', note: 'Floral offering' },
      { time: '11:00 AM', name: 'Bhog Arati', note: 'Community bhog' },
      { time: '8:00 PM', name: 'Sandhya Arati', note: 'Dhunuchi Nritya & finale' },
    ],
    accent: 'saffron',
  },
  {
    id: 6,
    date: 'Oct 21',
    day: 'Wednesday',
    title: 'Maha Dashami',
    sessions: [
      { time: '9:30 AM – 10:47 AM', name: 'Dashami Puja', note: 'Concluding rituals' },
      { time: '11:00 AM', name: 'Arati', note: 'Farewell arati' },
      { time: '11:30 AM', name: 'Devi Baran', note: 'Sindoor khela & vijaya' },
    ],
    accent: 'crimson',
  },
  {
    id: 7,
    date: 'Oct 25',
    day: 'Sunday',
    title: 'Mahalakshmi Puja',
    sessions: [
      { time: '7:00 PM – 10:00 PM', name: 'Lakshmi Puja', note: 'Evening rituals' },
      { time: '9:30 PM', name: 'Pushpanjali', note: 'Floral offering' },
      { time: '10:00 PM', name: 'Arati', note: 'Concluding arati' },
    ],
    accent: 'gold',
  },
];

export const luminaries = [
  {
    id: 1,
    name: 'Rabindranath Tagore',
    role: 'Poet · Nobel Laureate',
    quote: 'Faith is the bird that feels the light when the dawn is still dark.',
    image: 'https://www.bengaliassociationcoimbatore.com/wp-content/uploads/2015/07/ravindranath.png',
  },
  {
    id: 2,
    name: 'Swami Vivekananda',
    role: 'Philosopher · Monk',
    quote: 'Where can we go to find god, if we cannot see him in our own hearts and in every living being.',
    image: 'https://www.bengaliassociationcoimbatore.com/wp-content/uploads/2015/07/vivekanadar.png',
  },
  {
    id: 3,
    name: 'Kazi Nazrul Islam',
    role: 'Rebel Poet',
    quote: 'Continue your struggle against the monsters for the truth\'s sake; your name the world, forever, will take.',
    image: 'https://www.bengaliassociationcoimbatore.com/wp-content/uploads/2015/07/kazi.png',
  },
  {
    id: 4,
    name: 'Sarat Chandra Chattopadhyay',
    role: 'Novelist',
    quote: 'The fault lies not with the vision but with the closed windows. If you look out of only one opening, you\'ll never see anything new.',
    image: 'https://www.bengaliassociationcoimbatore.com/wp-content/uploads/2015/07/Sarat.png',
  },
];

export const committee = [
  { name: 'Mr. J. Dasgupta', role: 'A Few Words By Our Founding & Ex-President', tenure: '1993', initials: 'FP' },
  { name: 'Mr. Ayan Chatterjee', role: 'President', tenure: 'Current' },
  { name: 'Mr. Biswajit Paul', role: 'Vice President', tenure: 'Current' },
  { name: 'Mr. Sankar Samanta', role: 'Secretary', tenure: 'Current' },
];

// Message shown in the founder popup (opens when the Ex-President card is clicked)
export const founderMessage = [
  'The Bengali Association was formed, first informally and and subsequently as a big one as we see it today.',
  'A small Bengali community started the Durga Puja in 1992 on a small scale with the Pujo being held in Priya Kunj.',
  'It was the year I was transferred to Coimbatore and hence had the opportunity of joining the festive celebrations.',
  'There was no formal committee in 1992.',
  'In 1993, the Bengali association was formally formed and the Constitution was framed.',
  'I was privileged to head the newly formed association as the President and as a senior founder of the association, I continued to hold the post till 1996.',
  'Many of the organisers have since passed on and some have left Coimbatore and settled down elsewhere.',
  'By then the population of Bengalis had increased substantially.',
  'Some young and energetic people had also joined the association and I was now comfortable in handing over the baton to the next in line.',
  'The main agenda of the Association were Durga Puja and Lakshmi Puja.',
  'During those days all the members and their families used to participate in the celebrations and organise several cultural activities.',
  'The only drawback was that despite hosting the Pujo every year, we were unable to fix a permanent location for our Durga Puja.',
  'The Pujo continued to move locations with each passing year.',
  'Despite these shifts the members and their families loyally attended the celebrations every year.',
  'It was like a family getting together to celebrate the homecoming of their daughter Ma Durga and rejoicing in the festivities.',
  'From organising all 3 meals at the mantap to performing cultural programs on stage, the 5 days of Durga Puja were an example of unity and togetherness.',
  'Cultural activities were a daily affair with our in house women and children drama group performing with great passion and enthusiasm.',
  'Sometime in between a section of the members decided to separate themselves by forming another association.',
  'For getting the original name of the association, they went in for a long drawn litigation.',
  'This continued for years together after which the court decreed to the formation and naming of the 2 associations as they exist today.',
  'Many young members now came forward and fixed up SNV KALYANA MANDAPAM on a rental basis for performing the seasonal festivals. Rest of what has been happening now is well known to all the present members.',
  'I wish the association all success in their future progressive activities.',
  'May Goddess Durga bless us all...',
];

// Full board roster shown inside the "Board Members" popup
export const boardMembers = {
  management: [
    { role: 'President', name: 'Mr. Ayan Chatterjee' },
    { role: 'Vice President', name: 'Mr. Biswajit Paul' },
    { role: 'Secretary', name: 'Mr. Sankar Samanta' },
    { role: 'Treasurer', name: 'Mr. Puroshottam Purohit' },
  ],
  advisory: [
    { name: 'Mr. Vivekananda Pal' },
    { name: 'Mr. Pinku Das' },
    { name: 'Mr. Subrata Barik' },
    { name: 'Mr. Swaroop K Chattopadhyay' },
  ],
};

// General members shown inside the "Members" popup.
// Leave empty for now — add entries like { name: 'Full Name' } as they are finalized.
export const generalMembers = [];

// The Four Pillars of The Bengali Association Coimbatore
export const pillars = [
  {
    id: 1,
    number: '01',
    title: 'Durga Puja Celebration',
    tagline: 'The heart of our year',
    description: 'Durga Puja is the most cherished and eagerly awaited celebration of the Bengali Association, Coimbatore. Members and families come together with devotion, enthusiasm, and the traditional spirit of Bengal — through Maha Shashti, Saptami, Ashtami, Navami and Bijoya Dashami, with pujas, cultural programmes, devotional music, dance and community feasts.',
    quote: 'Pujo means togetherness — celebrating Maa Durga, celebrating Bengal, and celebrating our community.',
    icon: 'Flame',
    image: '/durga-puja-dhunuchi.webp',
  },
  {
    id: 2,
    number: '02',
    title: 'Community Services',
    tagline: 'Compassion in action',
    description: 'Beyond cultural activities, the Association believes in community, compassion and mutual support. Through Blood Donation Camps, Free Eye Checkup camps, Health Checkup drives and Annadanam, we promote social responsibility, volunteerism and collective welfare — supporting one another during times of need.',
    quote: 'Service is the truest form of prayer.',
    icon: 'HeartHandshake',
    image: '/community-feast.jpeg',
  },
  {
    id: 3,
    number: '03',
    title: 'Spreading Cultural Awareness',
    tagline: 'Roots for the next generation',
    description: 'We are committed to preserving, promoting and spreading awareness of Bengali culture and heritage. A special focus is placed on the younger generation — encouraging them to understand their roots and carry forward the language, traditions, values and cultural heritage of Bengal.',
    quote: 'A culture lives when its children remember it.',
    icon: 'Sparkles',
    image: '/cultural-sangeet.jpeg',
  },
  {
    id: 4,
    number: '04',
    title: 'Cultural Events & Get-Togethers',
    tagline: 'A year full of joy',
    description: 'From Durga Puja and Saraswati Puja to Kali Puja, annual picnics and traditional Bengali festivities — our year is stitched together with joy, friendship and togetherness. These occasions showcase our talents and pass our traditions to the next generation.',
    quote: 'Every gathering is a small festival of belonging.',
    icon: 'Users',
    image: '/events-football.webp',
  },
];

// Gallery categories: Puja, Community Services, Events, Media and Recognitions
export const galleryAlbums = [
  {
    id: 'puja',
    title: 'Puja',
    blurb: 'Durga Puja, Saraswati Puja & sacred rituals.',
    cover: '/durga-puja-dhunuchi.webp',
    photos: [
      '/gallery/puja/puja-1.jpeg',
      '/gallery/puja/puja-2.jpeg',
      '/gallery/puja/puja-3.jpeg',
      '/gallery/puja/puja-4.jpeg',
      '/gallery/puja/puja-5.jpeg',
    ],
  },
  {
    id: 'programs',
    title: 'Programs',
    blurb: 'Cultural nights, music, dance & performances.',
    cover: '/cultural-sangeet.jpeg',
    photos: [
      '/gallery/programs/prog-1.webp',
      '/gallery/programs/prog-2.webp',
      '/gallery/programs/prog-3.jpg',
      '/gallery/programs/prog-4.webp',
      '/gallery/programs/prog-5.jpeg',
    ],
  },
  {
    id: 'activities',
    title: 'Activities',
    blurb: 'Community service, sports & get-togethers.',
    cover: '/events-football.webp',
    photos: [
      '/gallery/activities/act-1.jpeg',
      '/gallery/activities/act-2.jpg',
      '/gallery/activities/act-3.jpg',
      '/gallery/activities/act-4.jpg',
      '/gallery/activities/act-5.jpg',
    ],
  },
  {
    id: 'news-media',
    title: 'News & Media',
    blurb: 'Press coverage, features & recognitions.',
    cover: '/community-group.webp',
    photos: [
      '/gallery/news/news-1.jpg',
      '/gallery/news/news-2.webp',
      '/gallery/news/news-3.jpg',
      '/gallery/news/news-4.webp',
      '/gallery/news/news-5.jpg',
    ],
  },
];

export const heritageCards = [
  {
    id: 1,
    title: 'Sahitya',
    subtitle: 'Literature',
    description: 'From Tagore to Bankim — the timeless words that shaped a civilization.',
    icon: 'BookOpen',
  },
  {
    id: 2,
    title: 'Sangeet',
    subtitle: 'Music',
    description: 'Rabindra Sangeet, Nazrul Geeti, Baul — melodies that carry the soul of Bengal.',
    icon: 'Music',
  },
  {
    id: 3,
    title: 'Nritya',
    subtitle: 'Dance',
    description: 'Dhunuchi, Kathak, and folk forms that ignite every celebration.',
    icon: 'Sparkles',
  },
  {
    id: 4,
    title: 'Rannaghor',
    subtitle: 'Cuisine',
    description: 'Shorshe Ilish, Kosha Mangsho, Mishti Doi — flavours steeped in tradition.',
    icon: 'UtensilsCrossed',
  },
];

export const testimonials = [
  {
    id: 1,
    name: 'Anindita Sen',
    role: 'Member since 2015',
    text: 'Every Durga Puja here feels like home. The warmth, the dhaak, the bhog — it is a piece of Kolkata in Coimbatore.',
  },
  {
    id: 2,
    name: 'Prasenjit Roy',
    role: 'Life Member',
    text: 'The association has stitched together a community that celebrates our roots while embracing the south. Truly special.',
  },
  {
    id: 3,
    name: 'Rupsa Mukherjee',
    role: 'Volunteer',
    text: 'From cultural functions to sindoor khela — the memories we create here are what our children will carry forward.',
  },
];

export const contact = {
  venue: 'The Bengali Association Coimbatore — Nakshtra Nivas',
  address: 'No. 12 Periyar Nagar, Masakalipalayam, Coimbatore – 641015',
  email: 'cbetba@gmail.com',
  phones: [
    { name: 'Mr. Ayan Chatterjee', number: '+91-9894280001' },
    { name: 'Mr. Shankar Samanta', number: '+91-7667559217' },
  ],
  socials: [
    { name: 'Facebook', href: 'https://www.facebook.com/tbacbe/' },
    { name: 'Instagram', href: 'https://www.instagram.com/thebengaliassociation.cbe/' },
  ],
};

export const navLinks = [
  { label: 'Home', href: '#home' },
  { label: 'About', href: '#about' },
  { label: 'Pillars', href: '#pillars' },
  { label: 'Schedule', href: '#events' },
  { label: 'Gallery', href: '#gallery' },
  { label: 'Committee', href: '#committee' },
  { label: 'Contact', href: '#contact' },
];

// Countdown target — Durga Puja 2026 Maha Saptami (Oct 17, 2026)
export const pujaDate = '2026-10-17T09:29:00';
