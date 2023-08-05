Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var types_1 = require("./types");
var EMAIL_REGEX = /[^@]+@[^\.]+\..+/;
function getUserKnownDataDetails(data, type) {
    switch (type) {
        case types_1.UserKnownDataType.NAME:
            return {
                subject: locale_1.t('Name'),
                value: data.name,
            };
        case types_1.UserKnownDataType.USERNAME:
            return {
                subject: locale_1.t('Username'),
                value: data.username,
            };
        case types_1.UserKnownDataType.ID:
            return {
                subject: locale_1.t('ID'),
                value: data.id,
            };
        case types_1.UserKnownDataType.IP_ADDRESS:
            return {
                subject: locale_1.t('IP Address'),
                value: data.ip_address,
            };
        case types_1.UserKnownDataType.EMAIL:
            return {
                subject: locale_1.t('Email'),
                value: data.email,
                subjectIcon: EMAIL_REGEX.test(data.email) && (<externalLink_1.default href={"mailto:" + data.email} className="external-icon">
            <icons_1.IconMail size="xs"/>
          </externalLink_1.default>),
            };
        default:
            return undefined;
    }
}
exports.default = getUserKnownDataDetails;
//# sourceMappingURL=getUserKnownDataDetails.jsx.map