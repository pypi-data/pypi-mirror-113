Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var qs = tslib_1.__importStar(require("query-string"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var documentationSetup_1 = tslib_1.__importDefault(require("./documentationSetup"));
var integrationSetup_1 = tslib_1.__importDefault(require("./integrationSetup"));
var otherSetup_1 = tslib_1.__importDefault(require("./otherSetup"));
var SdkConfiguration = function (props) {
    var parsed = qs.parse(window.location.search);
    var platform = props.platform;
    var integrationSlug = platform && integrationUtil_1.platfromToIntegrationMap[platform];
    // check for manual override query param
    if (integrationSlug && parsed.manual !== '1') {
        return <integrationSetup_1.default integrationSlug={integrationSlug} {...props}/>;
    }
    else if (platform === 'other') {
        return <otherSetup_1.default {...props}/>;
    }
    return <documentationSetup_1.default {...props}/>;
};
exports.default = SdkConfiguration;
//# sourceMappingURL=sdkConfiguration.jsx.map