Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var experimentConfig_1 = require("app/data/experimentConfig");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var experiments_1 = require("app/types/experiments");
var analytics_1 = require("app/utils/analytics");
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
/**
 * A HoC wrapper that injects `experimentAssignment` into a component
 *
 * This wrapper will automatically log exposure of the experiment upon
 * receiving the componentDidMount lifecycle event.
 *
 * For organization experiments, an organization object must be provided to the
 * component. You may wish to use the withOrganization HoC for this.
 *
 * If exposure logging upon mount is not desirable, The `injectLogExperiment`
 * option may be of use.
 *
 * NOTE: When using this you will have to type the `experimentAssignment` prop
 *       on your component. For this you should use the `ExperimentAssignment`
 *       mapped type.
 */
function withExperiment(Component, _a) {
    var _b;
    var experiment = _a.experiment, injectLogExperiment = _a.injectLogExperiment;
    return _b = /** @class */ (function (_super) {
            tslib_1.__extends(class_1, _super);
            function class_1() {
                var _this = _super !== null && _super.apply(this, arguments) || this;
                _this.logExperiment = function () {
                    return analytics_1.logExperiment({
                        key: experiment,
                        organization: _this.getProps().organization,
                    });
                };
                return _this;
            }
            // NOTE(ts): Because of the type complexity of this HoC, typescript
            // has a hard time understanding how to narrow Experiments[E]['type']
            // when we type assert on it.
            //
            // This means we have to do some typecasting to massage things into working
            // as expected.
            //
            // We DO guarantee the external API of this HoC is typed accurately.
            class_1.prototype.componentDidMount = function () {
                if (!injectLogExperiment) {
                    this.logExperiment();
                }
            };
            class_1.prototype.getProps = function () {
                return this.props;
            };
            Object.defineProperty(class_1.prototype, "config", {
                get: function () {
                    return experimentConfig_1.experimentConfig[experiment];
                },
                enumerable: false,
                configurable: true
            });
            Object.defineProperty(class_1.prototype, "experimentAssignment", {
                get: function () {
                    var type = this.config.type;
                    if (type === experiments_1.ExperimentType.Organization) {
                        var key = experiment;
                        return this.getProps().organization.experiments[key];
                    }
                    if (type === experiments_1.ExperimentType.User) {
                        var key = experiment;
                        return configStore_1.default.get('user').experiments[key];
                    }
                    return experimentConfig_1.unassignedValue;
                },
                enumerable: false,
                configurable: true
            });
            class_1.prototype.render = function () {
                var WrappedComponent = Component;
                var props = tslib_1.__assign(tslib_1.__assign({ experimentAssignment: this.experimentAssignment }, (injectLogExperiment ? { logExperiment: this.logExperiment } : {})), this.props);
                return <WrappedComponent {...props}/>;
            };
            return class_1;
        }(React.Component)),
        _b.displayName = "withExperiment[" + experiment + "](" + getDisplayName_1.default(Component) + ")",
        _b;
}
exports.default = withExperiment;
//# sourceMappingURL=withExperiment.jsx.map