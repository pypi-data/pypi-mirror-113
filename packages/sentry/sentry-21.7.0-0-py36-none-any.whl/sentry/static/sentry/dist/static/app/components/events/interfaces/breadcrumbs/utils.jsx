Object.defineProperty(exports, "__esModule", { value: true });
exports.transformCrumbs = void 0;
var tslib_1 = require("tslib");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var breadcrumbs_1 = require("app/types/breadcrumbs");
var utils_1 = require("app/utils");
function convertCrumbType(breadcrumb) {
    if (breadcrumb.type === breadcrumbs_1.BreadcrumbType.EXCEPTION) {
        return tslib_1.__assign(tslib_1.__assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.ERROR });
    }
    // special case for 'ui.' and `sentry.` category breadcrumbs
    // TODO: find a better way to customize UI around non-schema data
    if (breadcrumb.type === breadcrumbs_1.BreadcrumbType.DEFAULT && utils_1.defined(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.category)) {
        var _a = tslib_1.__read(breadcrumb.category.split('.'), 2), category = _a[0], subcategory = _a[1];
        if (category === 'ui') {
            return tslib_1.__assign(tslib_1.__assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.UI });
        }
        if (category === 'console') {
            return tslib_1.__assign(tslib_1.__assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.DEBUG });
        }
        if (category === 'navigation') {
            return tslib_1.__assign(tslib_1.__assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.NAVIGATION });
        }
        if (category === 'sentry' &&
            (subcategory === 'transaction' || subcategory === 'event')) {
            return tslib_1.__assign(tslib_1.__assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.TRANSACTION });
        }
    }
    if (!Object.values(breadcrumbs_1.BreadcrumbType).includes(breadcrumb.type)) {
        return tslib_1.__assign(tslib_1.__assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.DEFAULT });
    }
    return breadcrumb;
}
function getCrumbDetails(type) {
    switch (type) {
        case breadcrumbs_1.BreadcrumbType.USER:
        case breadcrumbs_1.BreadcrumbType.UI:
            return {
                color: 'purple300',
                icon: icons_1.IconUser,
                description: locale_1.t('User Action'),
            };
        case breadcrumbs_1.BreadcrumbType.NAVIGATION:
            return {
                color: 'green300',
                icon: icons_1.IconLocation,
                description: locale_1.t('Navigation'),
            };
        case breadcrumbs_1.BreadcrumbType.DEBUG:
            return {
                color: 'purple300',
                icon: icons_1.IconFix,
                description: locale_1.t('Debug'),
            };
        case breadcrumbs_1.BreadcrumbType.INFO:
            return {
                color: 'blue300',
                icon: icons_1.IconInfo,
                description: locale_1.t('Info'),
            };
        case breadcrumbs_1.BreadcrumbType.ERROR:
            return {
                color: 'red300',
                icon: icons_1.IconFire,
                description: locale_1.t('Error'),
            };
        case breadcrumbs_1.BreadcrumbType.HTTP:
            return {
                color: 'green300',
                icon: icons_1.IconSwitch,
                description: locale_1.t('HTTP request'),
            };
        case breadcrumbs_1.BreadcrumbType.WARNING:
            return {
                color: 'orange400',
                icon: icons_1.IconWarning,
                description: locale_1.t('Warning'),
            };
        case breadcrumbs_1.BreadcrumbType.QUERY:
            return {
                color: 'blue300',
                icon: icons_1.IconStack,
                description: locale_1.t('Query'),
            };
        case breadcrumbs_1.BreadcrumbType.SYSTEM:
            return {
                color: 'pink200',
                icon: icons_1.IconMobile,
                description: locale_1.t('System'),
            };
        case breadcrumbs_1.BreadcrumbType.SESSION:
            return {
                color: 'orange500',
                icon: icons_1.IconRefresh,
                description: locale_1.t('Session'),
            };
        case breadcrumbs_1.BreadcrumbType.TRANSACTION:
            return {
                color: 'pink300',
                icon: icons_1.IconSpan,
                description: locale_1.t('Transaction'),
            };
        default:
            return {
                icon: icons_1.IconTerminal,
                description: locale_1.t('Default'),
            };
    }
}
function transformCrumbs(breadcrumbs) {
    return breadcrumbs.map(function (breadcrumb, index) {
        var _a;
        var convertedCrumbType = convertCrumbType(breadcrumb);
        var crumbDetails = getCrumbDetails(convertedCrumbType.type);
        return tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({ id: index }, convertedCrumbType), crumbDetails), { level: (_a = convertedCrumbType === null || convertedCrumbType === void 0 ? void 0 : convertedCrumbType.level) !== null && _a !== void 0 ? _a : breadcrumbs_1.BreadcrumbLevelType.UNDEFINED });
    });
}
exports.transformCrumbs = transformCrumbs;
//# sourceMappingURL=utils.jsx.map