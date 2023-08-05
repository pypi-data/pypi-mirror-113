var _a;
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var integration_docs_platforms_1 = tslib_1.__importDefault(require("integration-docs-platforms"));
var locale_1 = require("app/locale");
var platformCategories_1 = require("./platformCategories");
var otherPlatform = {
    integrations: [
        {
            link: 'https://docs.sentry.io/platforms/',
            type: 'language',
            id: 'other',
            name: locale_1.t('Other'),
        },
    ],
    id: 'other',
    name: locale_1.t('Other'),
};
exports.default = (_a = []).concat.apply(_a, tslib_1.__spreadArray([[]], tslib_1.__read(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(integration_docs_platforms_1.default.platforms)), [otherPlatform]).map(function (platform) {
    return platform.integrations
        .map(function (i) { return (tslib_1.__assign(tslib_1.__assign({}, i), { language: platform.id })); })
        // filter out any tracing platforms; as they're not meant to be used as a platform for
        // the project creation flow
        .filter(function (integration) { return !platformCategories_1.tracing.includes(integration.id); });
}))));
//# sourceMappingURL=platforms.jsx.map