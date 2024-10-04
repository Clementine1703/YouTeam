<script setup>
import { ref, watch, onMounted } from 'vue';
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.css";
import { Russian } from "flatpickr/dist/l10n/ru.js";
import { english } from "flatpickr/dist/l10n/default.js";
import { Field, Form, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const props = defineProps(['language']);
const title = ref("Create Your account");
const placeholder = ref({
    lastName: "Enter Last Name",
    firstName: "Enter Name",
    middleName: "Enter Middle Name",
    gender: "Pick Gender",
    genderMale: "Male",
    genderFemale: "Female",
    genderNotSay: "Prefer not to say",
    dayOfBirth: "Day",
    monthOfBirth: "Month",
    yearOfBirth: "Year",
    email: "Enter Email",
    password: "Enter Password",
    phoneNumber: "Phone number",
    currentJobTitle: "Enter Job Title",
    experience: "Enter Year",
    itDomain: "Enter Primary IT Domain"
});
const titleField = ref({
    lastName: "Last Name",
    firstName: "Name",
    middleName: "Middle Name",
    gender: "Gender",
    dayOfBirth: "Day of birth",
    email: "Email",
    password: "Password",
    confirmPassword: "Confirm Password",
    phoneNumber: "Phone number",
    currentJobTitle: "Current Job Title",
    experience: "Experience",
    itDomain: "Primary IT Domain"
});
const buttonText = ref("Create an account");

const date = ref({
    day: ref(Array.from({ length: 31 }, (_, i) => 1 + i)),
    month: ref(Array.from({ length: 12 }, (_, i) => 1 + i)),
    year: ref(Array.from({ length: 100 }, (_, i) => new Date().getFullYear() - 99 + i)),
})


const userDate = ref({
    lastName: "",
    firstName: "",
    middleName: "",
    gender: "not-selected",
    dayOfBirth: {
        day: "not-selected",
        month: "not-selected",
        year: "not-selected"
    },
    phoneNumber: "",
    email: "",
    password: "",
    currentJobTitle: "",
    experience: "",
    itDomain: ""
});
const confirmPassword = ref("");
const errorMessages = ref({
    lastName: { required: "" },
    firstName: { required: "" },
    middleName: { required: "" },
    gender: { required: "" },
    dayOfBirth: { required: "" },
    phoneNumber: { required: "", matches: "" },
    email: { required: "", matches: "" },
    password: { required: "" },
    confirmPassword: { required: "" },
    currentJobTitle: { required: "" },
    tgLink: { required: "", matches: "" },
});
const createValidationSchema = (errorMessages) => {
    return yup.object({
        lastName: yup.string().required(errorMessages.value.lastName.required),
        firstName: yup.string().required(errorMessages.value.firstName.required),
        middleName: yup.string().required(errorMessages.value.middleName.required),
        gender: yup.string().test("not-selected", errorMessages.value.gender.required, value => value !== "not-selected")
            .required(errorMessages.value.gender.required),
        dayOfBirth: yup.object().shape({
            day: yup.string(),
            month: yup.string(),
            year: yup.string(),
        }).test("valid-date", errorMessages.value.dayOfBirth.required, (value) => {
            return value.day !== "not-selected" && value.month !== "not-selected" && value.year !== "not-selected";
        }),
        phoneNumber: yup.string().matches(/^\+?[1-9]\d{1,14}$/, errorMessages.value.phoneNumber.matches).required(errorMessages.value.phoneNumber.required),
        email: yup.string().email(errorMessages.value.email.matches).required(errorMessages.value.email.required),
        password: yup.string().required(errorMessages.value.password.required),
        confirmPassword: yup.string().required(errorMessages.value.confirmPassword.required),
    });
}
const validationSchema = ref(createValidationSchema(errorMessages));

const changeLanguage = () => {
    if (props.language === "en") {
        title.value = "Create Your account";
        placeholder.value = {
            lastName: "Enter Last Name",
            firstName: "Enter Name",
            middleName: "Enter Middle Name",
            gender: "Pick Gender",
            genderMale: "Male",
            genderFemale: "Female",
            genderNotSay: "Prefer not to say",
            dayOfBirth: "Day",
            monthOfBirth: "Month",
            yearOfBirth: "Year",
            email: "Enter Email",
            password: "Enter Password",
            phoneNumber: "Enter Phone number",
            currentJobTitle: "Enter Job Title",
            experience: "Enter Year",
            itDomain: "Enter Primary IT Domain"
        };
        titleField.value = {
            lastName: "Last Name",
            firstName: "Name",
            middleName: "Middle Name",
            gender: "Gender",
            dayOfBirth: "Day of birth",
            email: "Email",
            password: "Password",
            confirmPassword: "Confirm Password",
            phoneNumber: "Phone number",
            currentJobTitle: "Job Title",
            experience: "Experience",
            itDomain: "Primary IT Domain"
        };
        buttonText.value = "Create an account";
        errorMessages.value = {
            lastName: { required: "Last name is required!" },
            firstName: { required: "First name is required!" },
            middleName: { required: "Middle Name is required!" },
            gender: { required: "Please specify your gender!" },
            dayOfBirth: { required: "Date of birth is required!" },
            phoneNumber: { required: "Phone number is required!", matches: "Invalid phone number format" },
            email: { required: "Email is required!", matches: "Invalid email format" },
            password: { required: "Password is required!" },
            confirmPassword: { required: "Confirm Password is required!" },
            tgLink: { required: "Telegram link is required!", matches: "Invalid format. It should be either https://t.me/username or @username" },
            currentJobTitle: { required: "Current job title is required!" }
        };
    } else if (props.language === "ru") {
        title.value = "Создайте ваш аккаунт";
        placeholder.value = {
            lastName: "Введите Фамилию",
            firstName: "Введите Имя",
            middleName: "Введите Отчество",
            gender: "Укажите пол",
            genderMale: "Мужской",
            genderFemale: "Женский",
            genderNotSay: "Предпочитаю не указывать",
            dayOfBirth: "День",
            monthOfBirth: "Месяц",
            yearOfBirth: "Год",
            email: "Укажите Почту",
            password: "Введите Пароль",
            phoneNumber: "Введите Номер телефона",
            currentJobTitle: "Укажите текущее место работы",
            experience: "Укажите опыт работы",
            itDomain: "Укажите IT-домен"
        };
        titleField.value = {
            lastName: "Фамилия",
            firstName: "Имя",
            middleName: "Отчество",
            gender: "Пол",
            dayOfBirth: "День рождения",
            email: "Почта",
            password: "Пароль",
            confirmPassword: "Подтверждение",
            phoneNumber: "Номер телефона",
            currentJobTitle: "Текущее место работы",
            experience: "Опыт работы",
            itDomain: "IT-домен"
        };
        buttonText.value = "Создать аккаунт";
        errorMessages.value = {
            lastName: { required: "Фамилия обязательна!" },
            firstName: { required: "Имя обязательно!" },
            middleName: { required: "Отчество обязательно!" },
            gender: { required: "Пожалуйства укажите ваш пол!" },
            dayOfBirth: { required: "Дата рождения обязательна!" },
            phoneNumber: { required: "Номер телефона обязателен!", matches: "Неверный формат номера телефона" },
            email: { required: "Почта обязательна!", matches: "Неверный формат почты" },
            password: { required: "Пароль обязательный!" },
            confirmPassword: { required: "Подтверждение пароля обязательно!" },
            tgLink: { required: "Ссылка на Telegram обязательна!", matches: "Неверный формат ссылки. Ссылка должна быть вида https://t.me/username или @username" },
            currentJobTitle: { required: "Текущая должность обязательна" }
        };
    }
    validationSchema.value = createValidationSchema(errorMessages);

    flatpickr("#date-picker", {
        locale: props.language === "ru" ? Russian : english,
        dateFormat: "d.m.Y",
        disableMobile: true
    });
};

const userDateClear = () => {
    userDate.value = {
        lastName: "",
        firstName: "",
        middleName: "",
        gender: "not-selected",
        dayOfBirth: {
            day: "not-selected",
            month: "not-selected",
            year: "not-selected"
        },
        phoneNumber: "",
        email: "",
        tgLink: ""
    };
};

const sentUserDate = async () => {
    console.log(userDate.value);
    try {
        const response = await fetch("НУЖНО ВПИСАТЬ URL!", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userDate.value)
        });

        if (response.ok) {
            userDateClear();
            console.log("Форма успешно отправлена!");
        } else {
            console.error("Ошибка отправки формы:", response.statusText);
        }
    } catch (error) {
        console.error("Ошибка:", error);
    }
};

function showMenu() {
    document.querySelector(".registration").style.display = "flex";
}

function closeMenu() {
    document.querySelector(".registration").style.display = "none";
}

function openPage(event) {
    const numberPage = Number(event.target.getAttribute("numberPage"));
    const pages = document.querySelectorAll(".registration__page");
    const pageButtons = document.querySelector(".registration__buttons-page").children;
    for (let i = 0; i < pages.length; i++) {
        if (numberPage !== i) {
            pages[i].style.display = "none";
            pageButtons[i].classList.add("no-active");
            pageButtons[i].classList.remove("active");
        } else {
            pages[i].style.display = "flex";
            pageButtons[i].classList.add("active");
            pageButtons[i].classList.remove("no-active");
        }
    }
}

function updateDay() {
    if (!isNaN(Number(userDate.value.dayOfBirth.month)) && !isNaN(Number(userDate.value.dayOfBirth.year))) {
        const daysInMonth = new Date(Number(userDate.value.dayOfBirth.year), Number(userDate.value.dayOfBirth.month), 0).getDate();
        date.value.day = Array.from({length: daysInMonth}, (_, i) => 1 + i);
        console.log(date.value);
    }
}

watch(() => props.language, changeLanguage);
watch(
    () => [userDate.value.dayOfBirth.month, userDate.value.dayOfBirth.year],
    updateDay
);

onMounted(() => {
    changeLanguage();
});
defineExpose({ showMenu });
</script>

<template>
    <div class="registration">
        <div class="registration__background">
            <div class="registration__menu">
                <div class="registration__menu__navigation">
                    <button>
                        <svg width="16.500000" height="16.509766" viewBox="0 0 16.5 16.5098" fill="none"
                            xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                            <desc>
                                Created with Pixso.
                            </desc>
                            <defs />
                            <path id="Vector" d="M1.25 8.25L15.25 8.25M8.25 1.25L1.25 8.25L8.25 15.25" stroke="#FFFFFF"
                                stroke-opacity="1.000000" stroke-width="2.500000" stroke-linejoin="round"
                                stroke-linecap="round" />
                        </svg>
                    </button>
                    <button @click="closeMenu">
                        <svg width="15.843506" height="15.843750" viewBox="0 0 15.8435 15.8438" fill="none"
                            xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                            <desc>
                                Created with Pixso.
                            </desc>
                            <defs />
                            <path id="Vector" d="M1.25 1.25L14.58 14.58M1.25 14.58L14.58 1.25" stroke="#FFFFFF"
                                stroke-opacity="1.000000" stroke-width="2.500000" stroke-linejoin="round"
                                stroke-linecap="round" />
                        </svg>
                    </button>
                </div>
                <h1 class="registration__title">{{ title }}</h1>
                <div class="registration__form">
                    <Form class="registration__data" @submit="sentUserDate" :validation-schema="validationSchema">
                        <div class="registration__field">
                            <div class="registration__page">
                                <div class="registration__social-network">
                                    <button>
                                        <svg width="32.015381" height="38.000000" viewBox="0 0 32.0154 38" fill="none"
                                            xmlns="http://www.w3.org/2000/svg"
                                            xmlns:xlink="http://www.w3.org/1999/xlink">
                                            <desc>
                                                Created with Pixso.
                                            </desc>
                                            <defs />
                                            <path id="Vector"
                                                d="M26.67 36.47C24.6 38.48 22.34 38.16 20.17 37.21C17.87 36.24 15.76 36.2 13.33 37.21C10.29 38.52 8.69 38.14 6.87 36.47C-3.43 25.85 -1.91 9.68 9.78 9.09C12.63 9.24 14.62 10.65 16.28 10.78C18.78 10.27 21.16 8.82 23.82 9.01C27.01 9.26 29.41 10.53 31 12.81C24.41 16.76 25.97 25.43 32.01 27.86C30.81 31.02 29.25 34.17 26.65 36.49L26.67 36.47ZM16.07 8.97C15.76 4.26 19.58 0.37 23.97 0C24.58 5.44 19.03 9.49 16.07 8.97Z"
                                                fill="#898989" fill-opacity="1.000000" fill-rule="nonzero" />
                                        </svg>
                                    </button>
                                    <button>
                                        <svg width="32.000000" height="31.225098" viewBox="0 0 32 31.2251" fill="none"
                                            xmlns="http://www.w3.org/2000/svg"
                                            xmlns:xlink="http://www.w3.org/1999/xlink">
                                            <desc>
                                                Created with Pixso.
                                            </desc>
                                            <defs />
                                            <path id="Vector"
                                                d="M16 0C13.89 0 11.81 0.41 9.87 1.21C7.93 2.02 6.17 3.2 4.68 4.68C1.68 7.68 0 11.75 0 16C0 23.07 4.59 29.07 10.94 31.2C11.74 31.32 12 30.83 12 30.39L12 27.69C7.56 28.65 6.62 25.55 6.62 25.55C5.88 23.69 4.84 23.2 4.84 23.2C3.39 22.2 4.95 22.24 4.95 22.24C6.56 22.35 7.4 23.88 7.4 23.88C8.8 26.31 11.15 25.6 12.06 25.21C12.2 24.17 12.62 23.47 13.07 23.07C9.52 22.67 5.79 21.29 5.79 15.2C5.79 13.42 6.39 12 7.43 10.86C7.28 10.46 6.71 8.79 7.6 6.64C7.6 6.64 8.94 6.2 12 8.27C13.26 7.91 14.63 7.74 16 7.74C17.36 7.74 18.73 7.91 20 8.27C23.05 6.2 24.39 6.64 24.39 6.64C25.28 8.79 24.72 10.46 24.56 10.86C25.6 12 26.2 13.42 26.2 15.2C26.2 21.31 22.46 22.65 18.89 23.05C19.47 23.55 20 24.52 20 26.01L20 30.39C20 30.83 20.25 31.34 21.07 31.2C27.42 29.05 32 23.07 32 16C32 13.89 31.58 11.81 30.78 9.87C29.97 7.93 28.79 6.17 27.31 4.68C25.82 3.2 24.06 2.02 22.12 1.21C20.18 0.41 18.1 0 16 0Z"
                                                fill="#898989" fill-opacity="1.000000" fill-rule="nonzero" />
                                        </svg>
                                    </button>
                                    <button>
                                        <svg width="32.000000" height="32.000000" viewBox="0 0 32 32" fill="none"
                                            xmlns="http://www.w3.org/2000/svg"
                                            xmlns:xlink="http://www.w3.org/1999/xlink">
                                            <desc>
                                                Created with Pixso.
                                            </desc>
                                            <defs />
                                            <rect id="Registration/Google" rx="0.666667" width="30.666666"
                                                height="30.666666" transform="translate(0.666667 0.666667)"
                                                fill="#FFFFFF" fill-opacity="0" />
                                            <path id="Vector"
                                                d="M29.07 13.38L27.99 13.38L27.99 13.33L15.99 13.33L15.99 18.66L23.53 18.66C22.43 21.77 19.48 24 15.99 24C11.58 24 7.99 20.41 7.99 16C7.99 11.58 11.58 8 15.99 8C18.03 8 19.89 8.76 21.3 10.02L25.07 6.25C22.69 4.03 19.51 2.66 15.99 2.66C8.63 2.66 2.66 8.63 2.66 16C2.66 23.36 8.63 29.33 15.99 29.33C23.36 29.33 29.33 23.36 29.33 16C29.33 15.1 29.24 14.23 29.07 13.38Z"
                                                fill="#FFC107" fill-opacity="1.000000" fill-rule="nonzero" />
                                            <path id="Vector"
                                                d="M4.2 9.79L8.58 13C9.77 10.07 12.64 8 16 8C18.03 8 19.89 8.76 21.3 10.02L25.07 6.25C22.69 4.03 19.51 2.66 16 2.66C10.87 2.66 6.43 5.55 4.2 9.79Z"
                                                fill="#FF3D00" fill-opacity="1.000000" fill-rule="nonzero" />
                                            <path id="Vector"
                                                d="M16 29.33C19.44 29.33 22.57 28.01 24.93 25.87L20.81 22.37C19.42 23.43 17.73 24 16 24C12.53 24 9.58 21.78 8.47 18.7L4.12 22.05C6.33 26.37 10.81 29.33 16 29.33Z"
                                                fill="#4CAF50" fill-opacity="1.000000" fill-rule="nonzero" />
                                            <path id="Vector"
                                                d="M29.07 13.38L28 13.38L28 13.33L16 13.33L16 18.66L23.53 18.66C23 20.14 22.06 21.43 20.81 22.38L20.81 22.37L24.93 25.87C24.64 26.13 29.33 22.66 29.33 16C29.33 15.1 29.24 14.23 29.07 13.38Z"
                                                fill="#1976D2" fill-opacity="1.000000" fill-rule="nonzero" />
                                        </svg>
                                    </button>
                                </div>
                                <div class="registration__line-separator">
                                    <hr>
                                    <p>OR</p>
                                    <hr>
                                </div>
                                <div class="registration__page__inputs">
                                    <div class="registration__input">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.firstName }}</h1>
                                            <Field class="registration__input__field" v-model="userDate.firstName"
                                                :placeholder="placeholder.firstName" name="firstName" />
                                        </div>
                                        <ErrorMessage class="registration__input__error" name="firstName" />
                                    </div>
                                    <div class="registration__input">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.middleName }}</h1>
                                            <Field class="registration__input__field" v-model="userDate.middleName"
                                                :placeholder="placeholder.middleName" name="middleName" />
                                        </div>
                                        <ErrorMessage class="registration__input__error" name="middleName" />
                                    </div>
                                    <div class="registration__input">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.lastName }}</h1>
                                            <Field class="registration__input__field" v-model="userDate.lastName"
                                                :placeholder="placeholder.lastName" name="lastName" />
                                        </div>
                                        <ErrorMessage class="registration__input__error" name="lastName" />
                                    </div>
                                    <div class="registration__input">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.gender }}</h1>
                                            <Field as="select" v-model="userDate.gender"
                                                class="registration__input__field" id="gender" name="gender"
                                                rules="required">
                                                <option value="not-selected">{{ placeholder.gender }}</option>
                                                <option value="male">{{ placeholder.genderMale }}</option>
                                                <option value="female">{{ placeholder.genderFemale }}</option>
                                                <option value="prefer-not-to-say">{{ placeholder.genderNotSay }}
                                                </option>
                                            </Field>
                                        </div>
                                        <ErrorMessage class="registration__input__error" name="gender" />
                                    </div>
                                    <div class="registration__input registration__date">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.dayOfBirth }}</h1>
                                            <div class="registration__input registration__date__selects">
                                                <Field as="select" v-model="userDate.dayOfBirth.day"
                                                    class="registration__input__field" name="dayOfBirth.day">
                                                    <option value="not-selected">{{ placeholder.dayOfBirth }}</option>
                                                    <option v-for="day in date.day" :key="day" :value="day">{{ day }}</option>
                                                </Field>
                                                <Field as="select" v-model="userDate.dayOfBirth.month"
                                                    class="registration__input__field" name="dayOfBirth.month">
                                                    <option value="not-selected">{{ placeholder.monthOfBirth }}</option>
                                                    <option v-for="month in date.month" :month :value="month">{{ month }}</option>
                                                </Field>
                                                <Field as="select" v-model="userDate.dayOfBirth.year"
                                                    class="registration__input__field" name="dayOfBirth.year">
                                                    <option value="not-selected">{{ placeholder.yearOfBirth }}</option>
                                                    <option v-for="year in date.year" :key="year" :value="year">{{ year }}</option>
                                                </Field>
                                            </div>
                                        </div>
                                        <ErrorMessage class="registration__input__error" name="dayOfBirth" />
                                    </div>
                                </div>
                                <div class="registration__buttons-page">
                                    <button class="active" numberPage="0" @click="openPage" type="button"></button>
                                    <button class="no-active" numberPage="1" @click="openPage" type="button"></button>
                                    <button class="no-active" numberPage="2" @click="openPage" type="button"></button>
                                </div>
                                <button class="registration__button-next" numberPage="1" @click="openPage"
                                    type="button">Next</button>
                            </div>
                            <div class="registration__page">
                                <div class="registration__page__inputs">
                                    <div class="registration__input registration__input_email">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.email }}</h1>
                                            <Field class="registration__input__field" v-model="userDate.email"
                                                :placeholder="placeholder.email" name="email" />
                                        </div>
                                        <ErrorMessage class="registration__input__error" name="email" />
                                    </div>
                                    <div class="registration__input">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.password }}</h1>
                                            <Field class="registration__input__field" v-model="userDate.password"
                                                :placeholder="placeholder.password" name="password" />
                                        </div>
                                        <ErrorMessage class="registration__input__error" name="password" />
                                    </div>
                                    <div class="registration__input">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.confirmPassword }}</h1>
                                            <Field class="registration__input__field" v-model="confirmPassword"
                                                :placeholder="placeholder.password" name="confirmPassword" />
                                        </div>
                                        <ErrorMessage class="registration__input__error" name="confirmPassword" />
                                    </div>
                                    <div class="registration__input registration__input_phone">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.phoneNumber }}</h1>
                                            <Field class="registration__input__field" v-model="userDate.phoneNumber"
                                                :placeholder="placeholder.phoneNumber" name="phoneNumber" />
                                        </div>
                                        <ErrorMessage class="registration__input__error" name="phoneNumber" />
                                    </div>
                                </div>
                                <div class="registration__buttons-page">
                                    <button class="no-active" numberPage="0" @click="openPage" type="button"></button>
                                    <button class="active" numberPage="1" @click="openPage" type="button"></button>
                                    <button class="no-active" numberPage="2" @click="openPage" type="button"></button>
                                </div>
                                <button class="registration__button-next" numberPage="2" @click="openPage"
                                    type="button">Continue</button>
                            </div>
                            <div class="registration__page">
                                <div class="registration__page__inputs registration__page__inputs_last">
                                    <div class="registration__input registration__input_job-title">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.currentJobTitle }}</h1>
                                            <Field class="registration__input__field" v-model="userDate.currentJobTitle"
                                                :placeholder="placeholder.currentJobTitle" name="currentJobTitle" />
                                        </div>
                                        <ErrorMessage class="registration__input__error" name="currentJobTitle" />
                                    </div>
                                    <div class="registration__input">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.experience }}</h1>
                                            <select class="registration__input__field" name="experience">
                                                <option value="not-selected">{{ placeholder.experience }}</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="registration__input">
                                        <div class="registration__input__inside">
                                            <h1 class="registration__input__title">{{ titleField.itDomain }}</h1>
                                            <select class="registration__input__field" name="primary-it-domain">
                                                <option value="not-selected">{{ placeholder.itDomain }}</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="registration__buttons-page">
                                    <button class="no-active" numberPage="0" @click="openPage" type="button"></button>
                                    <button class="no-active" numberPage="1" @click="openPage" type="button"></button>
                                    <button class="active" numberPage="2" @click="openPage" type="button"></button>
                                </div>
                                <button class="registration__button-next" type="submit">{{ buttonText }}</button>
                                <label class="registration__privacy-policy" for="privacy-policy">
                                    <input id="privacy-policy" type="checkbox">
                                    <p>I agree to the <a href="#">Terms and Conditions</a> and <a href="#">Privacy
                                            Policy.</a></p>
                                </label>
                            </div>
                        </div>
                    </Form>
                </div>
            </div>
        </div>
        <!-- <pre style="background-color: green;">{{ errorMessages }}</pre> -->
    </div>
</template>

<style lang="scss">
* {
    padding: 0;
    margin: 0;
    font-size: 16px;
    box-sizing: border-box;
}

.registration {
    display: none;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;

    &__background {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: end;
        backdrop-filter: blur(5px);
        background-color: rgba(0, 0, 0, 0);
    }

    &__menu {
        background-color: rgb(7, 8, 10);
        width: calc(100svw/3);
        min-width: 604px;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 65px 81px;
        gap: 85px;

        &__navigation {
            display: flex;
            width: 100%;
            justify-content: space-between;
            align-items: center;
        }
    }

    &__form {
        width: 100%;
    }

    &__title {
        padding-bottom: 1.25rem;
        font-size: 2rem;
        color: white;
    }

    &__data {
        display: flex;
        width: 100%;
        flex-direction: column;
        align-items: center;
        gap: 1rem;

        button {
            padding: 0.8rem 0.5rem;
            font-size: 1.2rem;
            width: 100%;
            background-color: white;
        }
    }

    &__field {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        width: 100%;

        input {
            padding: 0.5rem;
            font-size: 1.2rem;
            width: 100%;
        }

        input::placeholder {
            font-size: 1.2rem;
        }
    }

    &__page {
        display: flex;
        flex-direction: column;
        gap: 32px;
        width: 100%;

        &__inputs {
            display: grid;
            grid-column-gap: 14px;
            grid-row-gap: 32px;
            grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(3, 1fr);

            &_last {
                grid-template-rows: repeat(2, 1fr);
            }
        }
    }

    &__page:not(:first-child) {
        display: none;
    }

    &__social-network {
        display: flex;
        gap: 16px;
        width: 100%;

        button {
            display: flex;
            justify-content: center;
            align-items: center;
            width: calc((100% - 16px) / 3);
            padding: 16px;
            border: 1px solid rgb(50, 50, 54);
            border-radius: 16px;
            background-color: rgb(7, 8, 10);
        }
    }

    &__line-separator {
        display: flex;
        align-items: center;
        padding: 0 25.5px;
        gap: 5px;

        hr {
            border: 1px solid rgb(93, 93, 98);
            width: 100%;
        }

        p {
            font-family: "Inter", sans-serif;
            font-weight: 400;
            font-size: 18px;
            line-height: 23.05px;
            color: rgb(93, 93, 98);
        }
    }

    &__gender {
        display: flex;
        flex-direction: column;
    }

    &__buttons-page {
        display: flex;
        width: 100%;
        justify-content: center;
        gap: 9px;
        margin-top: 27px;

        button {
            border-radius: 18px;
            padding: 0;
        }

        .no-active {
            width: 10px;
            height: 10px;
            background-color: rgb(137, 137, 137);
        }

        .active {
            width: 45px;
            height: 10px;
            background-color: rgb(255, 255, 255);
        }
    }

    &__input {
        display: flex;
        align-items: center;
        position: relative;

        &__error {
            position: absolute;
            color: red;
            font-size: 0.8rem;
            top: 0;
            transform: translateY(-100%);
        }

        &__title {
            color: rgb(255, 255, 255);
            font-family: "Barlow", sans-serif;
            font-weight: 500;
            font-size: 24px;
            line-height: 34.5px;
            margin-bottom: 10px;
        }

        &__field {
            padding: 20px 16px !important;
            color: rgb(137, 137, 137);
            font-family: "Inter", sans-serif;
            font-size: 16px;
            font-weight: 400;
            line-height: 23.05px;
            box-sizing: border-box;
            border: 1px solid rgb(50, 50, 54);
            border-radius: 16px;
            background-color: rgb(50, 50, 54);
            width: 100%;
        }

        &__inside {
            width: 100%;
        }

        &_email,
        &_phone,
        &_job-title {
            grid-column: 1 / span 2;
        }
    }

    &__date {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: start;
        position: relative;
        width: 100%;
        grid-column: 1 / span 2;

        &__selects {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            width: 100%;
        }

        input {
            width: 100%;
        }

        svg {
            width: 2rem;
            height: 2rem;
            position: absolute;
            right: 0;
        }
    }

    &__button-next {
        background-color: rgb(230, 230, 230);
        border-radius: 14px;
        background: rgb(230, 230, 230);
        padding: 20px;
        color: rgb(7, 8, 10);
        font-family: "Inter", sans-serif;
        font-size: 18px;
        font-weight: 500;
        line-height: 22px;
    }

    &__privacy-policy {
        display: flex;
        height: 24px;
        color: white;
        gap: 8px;

        input {
            width: auto;
        }

        a {
            text-decoration: underline;
        }
    }
}

@media(max-width: 1024px) {
    * {
        font-size: 14px;
    }
}

@media(max-width: 768px) {
    * {
        font-size: 12px;
    }
}
</style>
