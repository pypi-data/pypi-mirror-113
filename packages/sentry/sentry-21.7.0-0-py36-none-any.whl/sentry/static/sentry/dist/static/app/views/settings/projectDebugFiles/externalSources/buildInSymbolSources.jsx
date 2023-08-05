Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var locale_1 = require("app/locale");
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
function BuildInSymbolSources(_a) {
    var api = _a.api, organization = _a.organization, builtinSymbolSourceOptions = _a.builtinSymbolSourceOptions, builtinSymbolSources = _a.builtinSymbolSources, projectSlug = _a.projectSlug;
    function getRequestMessages(builtinSymbolSourcesQuantity) {
        if (builtinSymbolSourcesQuantity > builtinSymbolSources.length) {
            return {
                successMessage: locale_1.t('Successfully added built-in repository'),
                errorMessage: locale_1.t('An error occurred while adding new built-in repository'),
            };
        }
        return {
            successMessage: locale_1.t('Successfully removed built-in repository'),
            errorMessage: locale_1.t('An error occurred while removing built-in repository'),
        };
    }
    function handleChange(value) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, successMessage, errorMessage, updatedProjectDetails, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = getRequestMessages(value.length), successMessage = _a.successMessage, errorMessage = _a.errorMessage;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + projectSlug + "/", {
                                method: 'PUT',
                                data: {
                                    builtinSymbolSources: value,
                                },
                            })];
                    case 2:
                        updatedProjectDetails = _c.sent();
                        projectActions_1.default.updateSuccess(updatedProjectDetails);
                        indicator_1.addSuccessMessage(successMessage);
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        indicator_1.addErrorMessage(errorMessage);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    return (<selectField_1.default name="builtinSymbolSources" label={locale_1.t('Built-in Repositories')} help={locale_1.t('Configures which built-in repositories Sentry should use to resolve debug files.')} value={builtinSymbolSources} onChange={handleChange} choices={builtinSymbolSourceOptions === null || builtinSymbolSourceOptions === void 0 ? void 0 : builtinSymbolSourceOptions.filter(function (source) { return !source.hidden; }).map(function (source) { return [source.sentry_key, locale_1.t(source.name)]; })} getValue={function (value) { return (value === null ? [] : value); }} flexibleControlStateSize multiple/>);
}
exports.default = BuildInSymbolSources;
//# sourceMappingURL=buildInSymbolSources.jsx.map